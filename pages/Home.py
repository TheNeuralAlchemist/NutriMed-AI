from utils import load_global_css

load_global_css()
"""Home page: hero, the two modes, how it works, planned features, safety, FAQ."""
import streamlit as st

STEPS = [
    ("Upload", "Add a medical report or a food label photo."),
    ("Extract", "AI reads the text that is visible."),
    ("Review", "You confirm or correct what was read."),
    ("Explore", "Read clear explanations and ask questions."),
    ("Save", "Download a summary to keep."),
]
WHY = [
    ("Plain language", "Lab terms and additive names, explained without jargon."),
    ("Honest about limits", "Answers separate what your document says from general education, and say when something cannot be determined."),
    ("You stay in control", "Built so you can review extracted data, download your summary, and delete your history."),
]
MEDI = ["Report upload (PDF, JPG, PNG)", "Test table with the report's own reference ranges", "Plain-language explanations", "Medication information", "Ask MediLens AI"]
NUTRI = ["Ingredient photo or manual entry", "Ingredient deep-dive cards", "Nutrition facts analyser", "Health concerns explorer", "Ask NutriLens AI"]
SAFETY = [
    "No diagnoses, prescriptions, or dosage advice.",
    "Exact values and units from your report are preserved; unreadable text is flagged, not guessed.",
    "Safety claims about ingredients cite sources such as WHO, ICMR and FSSAI.",
    "Demo mode uses fictional data only.",
]
FAQ = [
    ("Is NutriMed AI a doctor?", "No. It explains information in plain language. Decisions about diagnosis, treatment and medicines belong to your doctor or pharmacist."),
    ("Does it say whether a food ingredient is harmful?", "It describes what is known and how strong the evidence is. It does not call every additive harmful or every natural ingredient safe."),
    ("Is my report stored?", "The finished app will let you choose, and delete your data at any time. Storage is not built yet."),
    ("What works today?", "Only the home and About pages. MediLens, NutriLens and Health Insights are planned and labelled as such."),
]

st.markdown(
    "<div class='status'>Prototype in development. Phase 1 of 10 is done: project setup and home page. "
    "Pages marked as planned are not built yet.</div>",
    unsafe_allow_html=True,
)

st.markdown(
    "<section class='hero'><h1>Your Health. Your Food. Better Understanding.</h1>"
    "<p>One intelligent platform to understand your medical reports and discover what goes into the food you eat.</p></section>",
    unsafe_allow_html=True,
)
b1, b2, _ = st.columns([1, 1, 2])
b1.page_link("pages/MediLens.py", label="Explore MediLens", icon="🩺")
b2.page_link("pages/NutriLens.py", label="Explore NutriLens", icon="🥗")
st.write("")
c1, c2 = st.columns(2, gap="large")
with c1:
    st.markdown(
        "<div class='mode medi'><h3>MediLens</h3><p>Upload your medical report. Understand your test results, "
        "medical terminology, and medication information in simple language.</p></div>",
        unsafe_allow_html=True,
    )
    st.page_link("pages/MediLens.py", label="Open MediLens", icon="🩺")
with c2:
    st.markdown(
        "<div class='mode nutri'><h3>NutriLens</h3><p>Scan your packaged food. Discover its ingredients, additives, "
        "nutrition facts, and possible alternatives.</p></div>",
        unsafe_allow_html=True,
    )
    st.page_link("pages/nutrilens.py", label="Open NutriLens", icon="🥗")

st.header("How it works")
steps = "".join(f"<li><b>{t}:</b> <span>{d}</span></li>" for t, d in STEPS)
st.markdown(f"<ol class='steps'>{steps}</ol>", unsafe_allow_html=True)

st.header("Why NutriMed AI?")
why = "".join(f"<div class='why'><b>{t}</b><p>{d}</p></div>" for t, d in WHY)
st.markdown(why, unsafe_allow_html=True)

st.header("Planned features")
f1, f2 = st.columns(2, gap="large")
with f1:
    st.markdown("**MediLens**")
    st.markdown("\n".join(f"- {x}" for x in MEDI))
with f2:
    st.markdown("**NutriLens**")
    st.markdown("\n".join(f"- {x}" for x in NUTRI))

st.header("Privacy and safety")
items = "".join(f"<li>{s}</li>" for s in SAFETY)
st.markdown(f"<div class='panel'><ul>{items}</ul></div>", unsafe_allow_html=True)

st.header("Frequently asked questions")
for q, a in FAQ:
    with st.expander(q):
        st.write(a)
