import streamlit as st

st.set_page_config(
    page_title="RA's FactCheckAI",
    page_icon="🔎",
    layout="wide"
)

st.title("🔎 RA's FactCheckAI")
st.caption("AI-powered claim verification and evidence analysis")

claim = st.text_area(
    "Enter a statement to fact-check",
    placeholder="Example: Artificial intelligence will replace all software developers."
)

if st.button("Verify Claim", type="primary"):
    if claim.strip():
        st.info("Claim submitted successfully. Verification engine is coming next.")
    else:
        st.warning("Please enter a claim.")