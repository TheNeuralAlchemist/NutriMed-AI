import streamlit as st

st.set_page_config(page_title="NutriMed AI", page_icon="🩺", layout="wide")

import MediLens
import NutriLens
import insights
import history_page

PAGES = ["🏠 Home", "🩺 MediLens", "🥗 NutriLens", "📊 Health Insights", "📜 History"]

st.sidebar.title("🩺 NutriMed AI")
mode = st.sidebar.radio("Choose a page", PAGES)
st.sidebar.caption("Educational demo. Not medical advice. Use fictional data only.")

if mode == PAGES[0]:
    st.title("NutriMed AI")
    st.write("Understand medical reports and food labels in plain language.")
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("🩺 MediLens")
        st.write("Upload a lab report, get a simple explanation, and chat about it.")
    with c2:
        st.subheader("🥗 NutriLens")
        st.write("Upload a food label photo, see ingredient cards and a nutrition table.")
    st.info("Pick a page from the sidebar to begin.")
elif mode == PAGES[1]:
    MediLens.show()
elif mode == PAGES[2]:
    NutriLens.show()
elif mode == PAGES[3]:
    insights.show()
else:
    history_page.show()
