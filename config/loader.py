from dotenv import load_dotenv
import os

# Load .env once at startup
load_dotenv()

# You can also define defaults here if needed
APP_NAME = os.getenv("APP_NAME", "Social Media Statistic")

#===========================================================================

# Service Account Initilization
TYPE = os.getenv("TYPE")
PROJECT_ID = os.getenv("PROJECT_ID")
PRIVATE_KEY_ID = os.getenv("PRIVATE_KEY_ID")
PRIVATE_KEY = os.getenv("PRIVATE_KEY").replace("\\n", "\n")  # Handle newline characters
CLIENT_EMAIL = os.getenv("CLIENT_EMAIL")
CLIENT_ID = os.getenv("CLIENT_ID")
AUTH_URI = os.getenv("AUTH_URI")
TOKEN_URI = os.getenv("TOKEN_URI")
AUTH_PROVIDER_X509_CERT_URL = os.getenv("AUTH_PROVIDER_X509_CERT_URL")
CLIENT_X509_CERT_URL = os.getenv("CLIENT_X509_CERT_URL")
UNIVERSE_DOMAIN = os.getenv("UNIVERSE_DOMAIN")

# ACCOUNT_SHEET_ID = os.getenv("ACCOUNT_SHEET_ID", "")
# FB_GAINED_SHEET_ID = os.getenv("FB_GAINED_SHEET_ID", "")
# IG_GAINED_SHEET_ID = os.getenv("IG_GAINED_SHEET_ID", "")
# YT_GAINED_SHEET_ID = os.getenv("YT_GAINED_SHEET_ID", "")
# TW_GAINED_SHEET_ID = os.getenv("TW_GAINED_SHEET_ID", "")

TESTING_SHEET_ID = os.getenv("TESTING_SHEET_ID", "")