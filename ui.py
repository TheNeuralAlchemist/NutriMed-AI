"""Shared UI helpers used by every page."""
import streamlit as st

import config


def load_styles() -> None:
    css = config.STYLES_PATH.read_text(encoding="utf-8")
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def coming_soon(title: str, theme: str, phase: int, items: list[str]) -> None:
    """Honest placeholder for pages that are not built yet."""
    st.markdown(
        f"<div class='page-head {theme}'><h1>{title}</h1>"
        f"<p>Planned for Phase {phase}. Not built yet.</p></div>",
        unsafe_allow_html=True,
    )
    st.subheader("What will be here")
    for item in items:
        st.markdown(f"- {item}")
    st.info("This page is a placeholder. It does not analyse anything yet.")


def footer() -> None:
    st.markdown(
        f"<div class='footer'><b>Disclaimer:</b> {config.DISCLAIMER}<br>"
        "NutriMed AI is a college mini-project. All demo data is fictional.</div>",
        unsafe_allow_html=True,
    )
