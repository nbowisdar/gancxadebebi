from pathlib import Path

BASE_URL = "https://gancxadebebi.ge"
ADVERTS_URL = BASE_URL + "/ru/%D0%9E%D0%B1%D1%8A%D1%8F%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D1%8F"

print(f"ADVERTS_URL: {ADVERTS_URL}")

# Directories
BASE_DIR = Path(__file__).parent
RESULT_DIR = BASE_DIR / "results"
RESULT_DIR.mkdir(exist_ok=True)

# Script configuration
MAX_PAGES = 25
RUN_SCRIPT_EVERY_HOUR = 24
HEADLESS_BROWSER = True
