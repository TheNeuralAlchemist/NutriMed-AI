import streamlit as st

st.set_page_config(
    page_title="NutriMed AI | Health & Nutrition Workspace",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

import MediLens
import NutriLens
import insights
import history_page
import config

# Global visual system. All analysis functions and session-state logic remain in
# their original modules; this file controls navigation and the dashboard UI.
css_path = config.STYLES_PATH
if css_path.exists():
    st.markdown(f"<style>{css_path.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)

PAGES = [
    ("Overview", "🏠"),
    ("MediLens", "🩺"),
    ("NutriLens", "🥗"),
    ("Health Insights", "📊"),
    ("History", "🕘"),
]
PAGE_LABELS = [f"{icon}  {name}" for name, icon in PAGES]

if "nutrimed_page" not in st.session_state:
    st.session_state["nutrimed_page"] = PAGE_LABELS[0]

with st.sidebar:
    st.markdown(
        """
        <div class="sidebar-brand">
          <div class="brand-symbol">✚</div>
          <div>
            <div class="brand-name">NutriMed <span>AI</span></div>
            <div class="brand-caption">HEALTH INTELLIGENCE</div>
          </div>
        </div>
        <div class="sidebar-section-label">WORKSPACE</div>
        """,
        unsafe_allow_html=True,
    )
    selected = st.radio(
        "Navigate",
        PAGE_LABELS,
        key="nutrimed_page",
        label_visibility="collapsed",
    )
    st.markdown(
        """
        <div class="sidebar-bottom">
          <div class="sidebar-status"><span></span> Your workspace is ready</div>
          <div class="sidebar-disclaimer">Educational information only.<br>Not a substitute for professional medical advice.</div>
          <div class="sidebar-version">NUTRIMED AI · STUDENT PROJECT</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

page = PAGE_LABELS.index(selected)
page_name = PAGES[page][0]

# Compact workspace header shared by every view.
left, right = st.columns([5, 1])
with left:
    st.markdown(
        f'<div class="eyebrow">NUTRIMED AI <span>/</span> {page_name.upper()}</div>',
        unsafe_allow_html=True,
    )
with right:
    st.markdown('<div class="secure-pill">✦ PRIVATE SESSION</div>', unsafe_allow_html=True)

if page == 0:
    st.markdown(
        """
        <section class="dashboard-hero">
          <div class="hero-copy">
            <div class="hero-kicker"><span class="hero-kicker-dot"></span> YOUR PERSONAL HEALTH WORKSPACE</div>
            <h1>Understand your health.<br><em>Make informed choices.</em></h1>
            <p>Bring medical reports and food labels into one clear space. Explore the information, understand the details, and prepare better questions for your healthcare professional.</p>
          </div>
          <div class="hero-art" aria-hidden="true">
            <div class="orbit orbit-one"></div><div class="orbit orbit-two"></div>
            <div class="hero-cross">✚</div><div class="orbit-dot dot-one"></div><div class="orbit-dot dot-two"></div>
            <div class="hero-art-label">HEALTH<br>×<br>NUTRITION</div>
          </div>
        </section>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="section-heading"><div><div class="section-kicker">YOUR TOOLS</div><h2>Explore your workspace</h2><p>Choose a space to get started.</p></div></div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.markdown(
            """
            <div class="feature-card feature-med">
              <div class="feature-top"><div class="feature-icon">⌁</div><span class="feature-tag">01 / MEDICAL</span></div>
              <h3>MediLens</h3>
              <p>Understand the information in your medical report, from test values and reference ranges to clear explanations.</p>
              <div class="feature-meta"><span>PDF · TXT</span><span>REPORT UNDERSTANDING ↗</span></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Open MediLens", key="go_medi", use_container_width=True, type="primary"):
            st.session_state["nutrimed_page"] = PAGE_LABELS[1]
            st.rerun()
    with c2:
        st.markdown(
            """
            <div class="feature-card feature-nutri">
              <div class="feature-top"><div class="feature-icon">◉</div><span class="feature-tag">02 / NUTRITION</span></div>
              <h3>NutriLens</h3>
              <p>Explore packaged-food labels, understand ingredients, and review the nutrition information shown on the pack.</p>
              <div class="feature-meta"><span>JPG · PNG · WEBP</span><span>FOOD LABEL ANALYSIS ↗</span></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Open NutriLens", key="go_nutri", use_container_width=True):
            st.session_state["nutrimed_page"] = PAGE_LABELS[2]
            st.rerun()

    st.markdown('<div class="section-heading section-heading-spaced"><div><div class="section-kicker">CONNECTED THINKING</div><h2>See the bigger picture</h2><p>Bring information from both tools together for a guided comparison.</p></div></div>', unsafe_allow_html=True)
    a, b = st.columns([1.4, 1], gap="large")
    with a:
        st.markdown(
            """
            <div class="insight-banner">
              <div class="insight-symbol">✳</div>
              <div><div class="insight-label">03 / CROSS-REFERENCE</div><h3>Health Insights</h3>
              <p>Compare information from a medical report and a food label in one place. Generate educational insights to support conversations with a doctor or dietitian.</p></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with b:
        st.markdown(
            """
            <div class="mini-panel">
              <div class="mini-panel-icon">↺</div><div class="section-kicker">YOUR ACTIVITY</div>
              <h3>Pick up where you left off.</h3><p>Previously saved explanations and scans are available in your history.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    x, y = st.columns(2)
    with x:
        if st.button("Explore Health Insights  ↗", key="go_insights", use_container_width=True):
            st.session_state["nutrimed_page"] = PAGE_LABELS[3]
            st.rerun()
    with y:
        if st.button("View History  ↗", key="go_history", use_container_width=True):
            st.session_state["nutrimed_page"] = PAGE_LABELS[4]
            st.rerun()

    st.markdown(
        """
        <div class="how-section">
          <div class="section-kicker">SIMPLE BY DESIGN</div><h2>From information to understanding</h2>
          <div class="how-grid">
            <div><b>01</b><strong>Upload</strong><span>Add a report or food label.</span></div>
            <div><b>02</b><strong>Review</strong><span>Check the information extracted.</span></div>
            <div><b>03</b><strong>Understand</strong><span>Explore clear, plain-language explanations.</span></div>
            <div><b>04</b><strong>Save</strong><span>Download useful summaries for later.</span></div>
          </div>
        </div>
        <div class="safety-strip"><span>✦</span><div><b>Designed with safety in mind</b><p>NutriMed AI is an educational tool. It does not diagnose conditions, prescribe medication, or replace advice from qualified healthcare professionals.</p></div></div>
        <div class="app-footer">NUTRIMED AI <span>·</span> HEALTH & NUTRITION INTELLIGENCE <span class="footer-right">MADE FOR BETTER UNDERSTANDING</span></div>
        """,
        unsafe_allow_html=True,
    )

elif page == 1:
    MediLens.show()
elif page == 2:
    NutriLens.show()
elif page == 3:
    insights.show()
else:
    history_page.show()

if page != 0:
    st.markdown(
        '<div class="app-footer">NUTRIMED AI <span>·</span> HEALTH & NUTRITION INTELLIGENCE <span class="footer-right">EDUCATIONAL INFORMATION ONLY</span></div>',
        unsafe_allow_html=True,
    )
