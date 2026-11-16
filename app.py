import streamlit as st
from services.search_service import search_web
from services.factcheck_service import factcheck_claim
from database.db import init_db, save_fact_check, get_fact_checks

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


# Callback: preserve submitted claim and clear input
def submit_claim():
    st.session_state.submitted_claim = st.session_state.claim_input
    st.session_state.claim_input = ""


# Application UI
st.title("RA's FactCheckAI")
st.write("Verify claims using evidence and AI.")

st.text_area(
    "Enter a claim to fact-check",
    placeholder="Example: The Earth revolves around the Sun.",
    height=120,
    key="claim_input"
)

st.button(
    "Fact Check Claim",
    type="primary",
    on_click=submit_claim
)


# Process submitted claim
claim = st.session_state.pop("submitted_claim", None)

if claim is not None:

    if not claim.strip():
        st.warning("Please enter a claim first.")

    else:
        try:
            with st.spinner("Searching for evidence..."):
                results = search_web(claim)

            if not results:
                st.warning("No search results found.")

            else:
                with st.spinner("AI is analyzing the evidence..."):
                    result = factcheck_claim(claim, results)

                fact_check_id = save_fact_check(
                    claim,
                    result,
                    results
                )

                st.success(
                    f"Fact-check saved successfully! ID: {fact_check_id}"
                )

                st.divider()
                st.subheader("Fact Check Result")

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

                st.divider()
                st.subheader("Search Sources")

                for index, source in enumerate(results, start=1):
                    with st.expander(
                        f"{index}. {source.get('title', 'Untitled')}"
                    ):
                        st.write(source.get("snippet", ""))

                        link = source.get("link")

                        if link:
                            st.markdown(f"[Visit source]({link})")

        except Exception as error:
            st.error(f"Fact-checking failed: {error}")


# Fact-check history
st.divider()
st.subheader("Fact-check History")

history = get_fact_checks()

if history:
    for item in history:
        with st.expander(
            f"{item['id']} - {item['claim']} | {item['verdict']}"
        ):
            st.write("**Confidence:**", f"{item['confidence']:.0%}")
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
