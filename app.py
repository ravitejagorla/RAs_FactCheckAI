
import streamlit as st
from services.search_service import search_web
from services.factcheck_service import factcheck_claim

st.set_page_config(
    page_title="RA's FactCheckAI",
    page_icon="🔎",
    layout="centered"
)

st.title("RA's FactCheckAI")
st.write("Verify claims using evidence and AI.")

claim = st.text_area(
    "Enter a claim to fact-check",
    placeholder="Example: The Earth revolves around the Sun.",
    height=120
)

if st.button("Fact Check Claim", type="primary"):
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

                for item in result.limitations:
                    st.write(f"- {item}")

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
