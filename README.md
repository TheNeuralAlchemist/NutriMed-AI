# NutriMed AI

Dual-mode educational health app: **MediLens** (medical report understanding) and **NutriLens** (packaged-food ingredient analysis). Not a medical device. Does not diagnose or prescribe.

## Status
Phase 1 of 10 done (setup + home page). MediLens, NutriLens and Health Insights are labelled placeholders.

## Run
```
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # Windows: copy .env.example .env
streamlit run app.py
```
Open http://localhost:8501
