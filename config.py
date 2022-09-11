import os

TG_TOKEN = os.environ.get("TG_TOKEN", "NO-TOKEN")
WEB_HOOK_URL = os.environ.get("WEB_HOOK_URL", "NO URL")
WEB_HOOK_PORT = int(os.environ.get("PORT", "8443"))
VAX_DATA_URL = (
    "https://raw.githubusercontent.com/owid/covid-19-data/master/"
    + "public/data/vaccinations/vaccinations.json"
)

CASES_DATA_URL = (
    "https://raw.githubusercontent.com/owid/covid-19-data/master/"
    + "public/data/latest/owid-covid-latest.json"
)
