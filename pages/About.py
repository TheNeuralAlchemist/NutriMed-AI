from utils import load_global_css

load_global_css()
import streamlit as st

import config

st.title("About NutriMed AI")
st.write(
    "Medical reports and food labels are full of terms most people were never taught. "
    "NutriMed AI explains them in plain language so you can ask better questions and make better-informed choices."
)
st.subheader("What it is not")
st.markdown(
    "- Not a diagnosis, prescription, or dosage tool.\n"
    "- Not a replacement for doctors, pharmacists, dietitians, or emergency services.\n"
    "- Not able to confirm that a food is free of an allergen. Check with the manufacturer."
)
st.subheader("Sources we prioritise")
st.markdown("WHO, ICMR, FSSAI, other government health agencies, peer-reviewed literature, and official medicine information.")
st.info(config.DISCLAIMER)
