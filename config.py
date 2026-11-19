"""Central configuration for NutriMed AI. Secrets come from .env, never from code."""
import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).parent
load_dotenv(BASE_DIR / ".env")

APP_NAME = "NutriMed AI"
TAGLINE = "Understand Your Health. Know What You Eat."

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
MAX_UPLOAD_MB = int(os.getenv("MAX_UPLOAD_MB", "10"))
MEDICAL_FILE_TYPES = ["pdf", "jpg", "jpeg", "png"]
FOOD_FILE_TYPES = ["jpg", "jpeg", "png"]

DB_PATH = BASE_DIR / "database" / "nutrimed.db"
STYLES_PATH = BASE_DIR / "assets" / "styles.css"

DISCLAIMER = (
    "NutriMed AI is an educational information tool. It does not diagnose diseases, "
    "prescribe medicines, change dosages, or replace doctors, dietitians, pharmacists, "
    "or emergency services. In an emergency, contact your local emergency number."
)
