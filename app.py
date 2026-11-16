
import streamlit as st

from services.search_service import search_web
from services.factcheck_service import factcheck_claim
from services.claim_service import split_claims

from database.db import (
    init_db,
    save_fact_check,
    get_fact_checks
)


st.set_page_config(
    page_title="RA's FactCheckAI",
    page_icon="🔎",
    layout="centered"
)

init_db()


# Session state
if "claim_input" not in st.session_state:
    st.session_state.claim_input = ""

if "submitted_claim" not in st.session_state:
    st.session_state.submitted_claim = None


# Submit callback
def submit_claim():
    st.session_state.submitted_claim = st.session_state.claim_input
    st.session_state.claim_input = ""


# Application UI
st.title("RA's FactCheckAI")
st.write("Verify claims using evidence and AI.")

st.text_area(
    "Enter one or more claims",
    placeholder=(
        "India became independent in 1947.\n"
        "The Earth revolves around the Sun.\n"
        "Hyderabad is in Telangana."
    ),
    height=150,
    key="claim_input"
)

st.button(
    "Fact Check Claims",
    type="primary",
    on_click=submit_claim
)


# Process submitted input
submitted_text = st.session_state.pop("submitted_claim", None)

if submitted_text is not None:

    if not submitted_text.strip():
        st.warning("Please enter at least one claim.")

    else:
        try:
            with st.spinner("Extracting individual claims..."):
                claims = split_claims(submitted_text)

            if not claims:
                st.warning(
                    "No factual claims were detected. "
                    "Please enter factual statements instead of questions or opinions."
                )

            else:
                st.success(f"Detected {len(claims)} factual claim(s).")

                for index, claim in enumerate(claims, start=1):

                    st.divider()
                    st.header(f"Claim {index}")
                    st.write(claim)

                    try:
                        with st.spinner(f"Searching evidence for claim {index}..."):
                            results = search_web(claim)

                        if not results:
                            st.warning("No search results found for this claim.")
                            continue

                        with st.spinner(f"Analyzing claim {index}..."):
                            result = factcheck_claim(claim, results)

                        fact_check_id = save_fact_check(
                            claim,
                            result,
                            results
                        )

                        st.success(
                            f"Fact-check saved successfully! ID: {fact_check_id}"
                        )

                        col1, col2 = st.columns(2)

                        with col1:
                            st.metric("Verdict", result.verdict.value)

                        with col2:
                            st.metric(
                                "AI Confidence",
                                f"{result.confidence:.0%}"
                            )

                        st.subheader("Explanation")
                        st.write(result.explanation)

                        st.subheader("Supporting Evidence")

                        if result.supporting_evidence:
                            for item in result.supporting_evidence:
                                st.write(f"- {item}")
                        else:
                            st.info("No supporting evidence identified.")

                        st.subheader("Contradicting Evidence")

                        if result.contradicting_evidence:
                            for item in result.contradicting_evidence:
                                st.write(f"- {item}")
                        else:
                            st.info("No contradicting evidence identified.")

                        st.subheader("Limitations")

                        if result.limitations:
                            for item in result.limitations:
                                st.write(f"- {item}")
                        else:
                            st.info("No limitations reported.")

                        st.subheader("Search Sources")

                        for source_index, source in enumerate(
                            results,
                            start=1
                        ):
                            with st.expander(
                                f"{source_index}. "
                                f"{source.get('title', 'Untitled')}"
                            ):
                                st.write(source.get("snippet", ""))

                                link = source.get("link")

                                if link:
                                    st.markdown(
                                        f"[Visit source]({link})"
                                    )

                    except Exception as error:
                        st.error(
                            f"Fact-checking failed for claim {index}: {error}"
                        )

        except Exception as error:
            st.error(f"Claim extraction failed: {error}")


# Fact-check history
st.divider()
st.subheader("Fact-check History")

history = get_fact_checks()

if history:

    for item in history:

        with st.expander(
            f"{item['id']} - {item['claim']} | {item['verdict']}"
        ):

            st.write(
                "**Confidence:**",
                f"{item['confidence']:.0%}"
            )

            st.write("**Explanation:**", item["explanation"])

            st.write("**Supporting Evidence:**")

            for evidence in item["supporting_evidence"]:
                st.write(f"- {evidence}")

            st.write("**Sources:**")

            for source in item["sources"]:

                if source["url"]:
                    st.markdown(
                        f"[{source['title'] or 'Visit source'}]"
                        f"({source['url']})"
                    )

else:
    st.info("No previous fact-checks found.")
