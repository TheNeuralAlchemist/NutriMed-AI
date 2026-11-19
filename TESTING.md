# Test checklist (Phase 10)
Home/sidebar: all 5 pages open without errors.
MediLens: upload sample_data/fake_lab_report.txt -> text shows -> Explain -> PDF/TXT download -> ask 3 chat questions.
Bad files: .png in MediLens, empty file, file over 10 MB, scanned PDF -> red message, no crash.
NutriLens: upload a clear label photo -> Read -> cards + table -> PDF -> chat.
Bad photos: blurry photo, wrong type (.pdf), huge file -> friendly message.
Insights: needs both a report and a label.
History: entries appear; PDF works; Clear works.
Wrong/missing key: message tells you to fix .env (no crash).

# Go online
1. Put the project on GitHub WITHOUT .env and history.json.
2. share.streamlit.io -> New app -> pick repo, main file app.py.
3. Settings -> Secrets: GEMINI_API_KEY = "your_key"
4. Deploy.
