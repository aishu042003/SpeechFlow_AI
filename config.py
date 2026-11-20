from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
UPLOAD_DIR = DATA_DIR / "uploads"
DATABASE_DIR = DATA_DIR / "database"
REPORT_DIR = BASE_DIR / "reports"
DB_PATH = DATABASE_DIR / "speechflow.db"

APP_TITLE = "SpeechFlow AI"

COLORS = {
    "charcoal_black": "#171717",
    "forest_green": "#06110C",
    "crimson_red": "#A31C1B",
    "card": "#06110C",
    "sidebar": "#111111",
    "white": "#FFFFFF",
    "muted": "#A0A0A0",
}

for directory in (UPLOAD_DIR, DATABASE_DIR, REPORT_DIR):
    directory.mkdir(parents=True, exist_ok=True)