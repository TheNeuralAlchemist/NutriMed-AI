"""Phase 9: shows saved history."""
import streamlit as st
import history
from pdf_utils import make_pdf


def show():
    st.title("📜 History")
    items = history.load()
    if not items:
        st.info("Nothing saved yet. Your explanations and label scans will appear here.")
        return
    for i, it in enumerate(items):
        with st.expander(f"{it['time']}  |  {it['kind']}  |  {it['title']}"):
            st.text(it["content"])
            st.download_button("⬇️ PDF", make_pdf(f"{it['kind']} - {it['title']}", [(it["time"], it["content"])]),
                               file_name=f"history_{i}.pdf", mime="application/pdf", key=f"h{i}")
    if st.button("🗑️ Clear all history"):
        history.clear()
        st.rerun()
