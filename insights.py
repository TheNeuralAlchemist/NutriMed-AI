"""Phase 8: Health Insights compares MediLens and NutriLens."""
import json
import streamlit as st
import ai
import history
from pdf_utils import make_pdf


def show():
    st.title("📊 Health Insights")
    st.caption("Compares your report (MediLens) with your food label (NutriLens).")

    report = st.session_state.get("report_text")
    label = st.session_state.get("label_data")

    c1, c2 = st.columns(2)
    c1.metric("MediLens report", "Loaded" if report else "Missing")
    c2.metric("NutriLens label", "Loaded" if label else "Missing")

    if not report or not label:
        st.info("To see insights, first upload a report in MediLens and scan a label in NutriLens.")
        return

    if st.button("✨ Generate insights", type="primary"):
        prompt = (
            ai.SAFETY
            + "Compare the medical report and the food label below. Use these headings: "
              "1. What the report shows (short), 2. How this food fits with it, "
              "3. Simple tips, 4. Questions to ask a doctor or dietitian. "
              "Do not diagnose. Do not say the food is safe or unsafe for the person.\n\n"
              "--- REPORT ---\n" + report[:8000]
            + "\n--- FOOD LABEL ---\n" + json.dumps(label, ensure_ascii=False)[:6000]
        )
        with st.spinner("Comparing..."):
            answer, err = ai.ask(prompt)
        if err:
            st.error(err)
        else:
            st.session_state["insights"] = answer
            history.add("Insights", label.get("product_name") or "Insights", answer)

    answer = st.session_state.get("insights")
    if answer:
        st.markdown(answer)
        st.download_button("⬇️ Download PDF",
                           make_pdf("Health Insights", [("Insights", answer)]),
                           file_name="health_insights.pdf", mime="application/pdf")
