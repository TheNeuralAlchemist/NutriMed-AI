import streamlit as st
import ai
import chat
import history
from pdf_utils import make_pdf
from utils import extract_text


def show():
    st.title("🩺 MediLens")
    st.caption("Medical report assistant. Use fictional reports only.")
    metrics = st.container()  # filled at the end so the numbers are fresh

    tab_upload, tab_explain, tab_chat = st.tabs(["📄 Upload", "💡 Explanation", "💬 Chat"])

    # ---------- Phase 3: upload and extract text ----------
    with tab_upload:
        f = st.file_uploader("Upload a report (PDF or TXT, max 10 MB)",
                             type=["pdf", "txt"], key="report_uploader")
        if f is not None:
            text, err = extract_text(f)
            if err:
                st.error(err)
            elif text != st.session_state.get("report_text"):
                # new report: clear the old explanation and chat
                st.session_state["report_text"] = text
                st.session_state["report_name"] = f.name
                st.session_state.pop("report_explanation", None)
                st.session_state["chat_medilens"] = []
                st.success(f"Extracted text from {f.name}")
        if st.session_state.get("report_text"):
            st.text_area("Extracted text", st.session_state["report_text"], height=300)

    # ---------- Phase 4: plain-language explanation ----------
    with tab_explain:
        report = st.session_state.get("report_text")
        if not report:
            st.info("Upload a report first in the Upload tab.")
        else:
            if st.button("✨ Explain my report", type="primary"):
                prompt = (
                    ai.SAFETY
                    + "Explain this medical report to a person with no medical knowledge. "
                      "Use these headings: 1. Summary, 2. Values explained (each test: "
                      "what it measures, the person's value, and whether it is inside, "
                      "above or below the normal range given in the report), "
                      "3. Things to ask the doctor, 4. Healthy lifestyle ideas (general). "
                      "Do not diagnose.\n\n--- REPORT ---\n" + report[:15000]
                )
                with st.spinner("Reading your report..."):
                    answer, err = ai.ask(prompt)
                if err:
                    st.error(err)
                else:
                    st.session_state["report_explanation"] = answer
                    history.add("MediLens", st.session_state.get("report_name", "Report"), answer)

            explanation = st.session_state.get("report_explanation")
            if explanation:
                st.markdown(explanation)
                # ---------- Phase 9: downloads ----------
                title = f"MediLens explanation - {st.session_state.get('report_name', '')}"
                d1, d2 = st.columns(2)
                d1.download_button("⬇️ Download PDF",
                                   make_pdf(title, [("Explanation", explanation)]),
                                   file_name="medilens_explanation.pdf",
                                   mime="application/pdf")
                d2.download_button("⬇️ Download TXT", explanation,
                                   file_name="medilens_explanation.txt")

    # ---------- Phase 4: chat ----------
    with tab_chat:
        report = st.session_state.get("report_text")
        if not report:
            st.info("Upload a report first in the Upload tab.")
        else:
            chat.chat_ui("medilens", report, "medical report")

    with metrics:
        c1, c2, c3 = st.columns(3)
        c1.metric("Report loaded", "Yes" if st.session_state.get("report_text") else "No")
        c2.metric("Characters extracted", len(st.session_state.get("report_text", "")))
        c3.metric("Explanation", "Ready" if st.session_state.get("report_explanation") else "Pending")
