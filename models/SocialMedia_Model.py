from config.loader import (
    TYPE, PROJECT_ID, PRIVATE_KEY_ID, PRIVATE_KEY, CLIENT_EMAIL, CLIENT_ID,
    AUTH_URI, TOKEN_URI, AUTH_PROVIDER_X509_CERT_URL, CLIENT_X509_CERT_URL, UNIVERSE_DOMAIN,
    FB_GAINED_SHEET_ID, TESTING_SHEET_ID
)
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.service_account import Credentials
from calendar import monthrange
from datetime import datetime, timedelta


class SocialMedia_Model:
    def __init__(self, platform, brand, yesterday_date):
        self.platform = platform
        self.brand = brand.lower()
        self.yesterday_date = yesterday_date
        # self.range = range.lower()
        self.followers = None
        self.engagement = None
        self.impressions = None
        
        # Store data inside self
        self.currency = [] # all values in column A
        self.rows = []
        self.statistic = [] # row objects with index + value
        self.total_rows = 0

        self.scope = ["https://www.googleapis.com/auth/spreadsheets"]
        config_dict = {
            "type": TYPE,
            "project_id": PROJECT_ID,
            "private_key_id": PRIVATE_KEY_ID,
            "private_key": PRIVATE_KEY,
            "client_email": CLIENT_EMAIL,
            "client_id": CLIENT_ID,
            "auth_uri": AUTH_URI,
            "token_uri": TOKEN_URI,
            "auth_provider_x509_cert_url": AUTH_PROVIDER_X509_CERT_URL,
            "client_x509_cert_url": CLIENT_X509_CERT_URL,
            "universe_domain": UNIVERSE_DOMAIN,
        }
        self.creds = Credentials.from_service_account_info(config_dict, scopes=self.scope)
        self.service = build("sheets", "v4", credentials=self.creds)

    def number_to_column(self, n):
        """Convert 1-based column number to Excel/Sheets letter(s)"""
        result = ""
        n += 2
        original = n
        while n > 0:
            n, remainder = divmod(n - 1, 26)
            result = chr(65 + remainder) + result
        return result, original

    def analytics(self):
        """Fetch columns and map B-V rows with title, handle missing dates by filling 0"""
        if self.brand == "jeetbuzz":
            suspended_value = ["BDT", "PKR", "INR", "FACEBOOK NEW. INSTAGRAM ACCOUNT"]
        elif self.brand == "six6s":
            suspended_value = []
        elif self.brand == "badsha":
            suspended_value = []
        else:
            suspended_value = []

        sheet_id = FB_GAINED_SHEET_ID
        today = datetime.strptime(self.yesterday_date, "%d-%m-%Y")
        days_in_month = monthrange(today.year, today.month)[1]
        last_day_letter, corresponding_number = self.number_to_column(days_in_month + 1)
        range_a_v = f"{self.brand}!A:{last_day_letter}"

        def safe_int(val):
            """Convert to int if possible, else return 0"""
            val = val.strip()
            if val == "":
                return 0
            try:
                return int(val)
            except ValueError:
                return 0

        try:
            result = self.service.spreadsheets().values().get(
                spreadsheetId=sheet_id,
                range=range_a_v
            ).execute()

            raw = result.get("values", [])
            normalized = [(row + [""] * corresponding_number)[:corresponding_number] for row in raw]

            self.currency = []
            self.rows = []

            TITLE_MAP = {
                "TOTAL FOLLOWERS": "total_followers",
                "DAILY FOLLOWERS GAIN": "daily_followers_gain",
                "MONTHLY ENGAGEMENTS": "monthly_engagements",
                "DAILY ENGAGEMENTS": "daily_engagements",
                "MONTHLY IMPRESSIONS": "monthly_impressions",
                "DAILY IMPRESSIONS": "daily_impressions"
            }

            date_headers = [d.strip().lstrip("'") for d in normalized[0][3:]]  # first row has dates
            sheet_date_to_index = {date_headers[idx]: idx for idx in range(len(date_headers)) if date_headers[idx] != ""}

            for i, row in enumerate(normalized):
                value_a = row[0].strip()
                if value_a == "" or value_a.upper() in suspended_value:
                    continue

                self.currency.append(value_a)
                sheet_index = i + 1

                # Map row titles
                raw_title_followers = row[1].strip()
                if i + 1 >= len(normalized): continue
                daily_followers_gain_row = normalized[i + 1]
                raw_title_daily_followers = daily_followers_gain_row[1].strip()

                if i + 3 >= len(normalized): continue
                engagement_row = normalized[i + 3]
                raw_title_engagement = engagement_row[1].strip()

                if i + 2 >= len(normalized): continue
                daily_engagement_row = normalized[i + 2]
                raw_title_daily_engagement = daily_engagement_row[1].strip()

                if i + 6 >= len(normalized): continue
                impression_row = normalized[i + 6]
                raw_title_impression = impression_row[1].strip()

                if i + 5 >= len(normalized): continue
                daily_impression_row = normalized[i + 5]
                raw_title_daily_impression = daily_impression_row[1].strip()

                # Map titles to keys
                title_followers = TITLE_MAP.get(raw_title_followers)
                title_daily_followers = TITLE_MAP.get(raw_title_daily_followers)
                title_engagement = TITLE_MAP.get(raw_title_engagement)
                title_daily_engagement = TITLE_MAP.get(raw_title_daily_engagement)
                title_impression = TITLE_MAP.get(raw_title_impression)
                title_daily_impression = TITLE_MAP.get(raw_title_daily_impression)

                # --- SAFE NUMERIC PARSING ---
                numeric_followers = [safe_int(x) for x in row[3:]]
                numeric_daily_followers = [safe_int(x) for x in daily_followers_gain_row[3:]]
                numeric_engagements = [safe_int(x) for x in engagement_row[3:]]
                numeric_daily_engagements = [safe_int(x) for x in daily_engagement_row[3:]]
                numeric_impressions = [safe_int(x) for x in impression_row[3:]]
                numeric_daily_impressions = [safe_int(x) for x in daily_impression_row[3:]]

                # --- CREATE DATA WITH DATES, FILL MISSING WITH 0 ---
                label_objects = []
                current_date = today
                for _ in range(len(date_headers)):
                    date_str = current_date.strftime("%d/%m/%Y")
                    idx = sheet_date_to_index.get(date_str, None)
                    label_objects.append({
                        "date": date_str,
                        title_followers: numeric_followers[idx] if idx is not None and idx < len(numeric_followers) else 0,
                        title_daily_followers: numeric_daily_followers[idx] if idx is not None and idx < len(numeric_daily_followers) else 0,
                        title_daily_engagement: numeric_daily_engagements[idx] if idx is not None and idx < len(numeric_daily_engagements) else 0,
                        title_engagement: numeric_engagements[idx] if idx is not None and idx < len(numeric_engagements) else 0,
                        title_daily_impression: numeric_daily_impressions[idx] if idx is not None and idx < len(numeric_daily_impressions) else 0,
                        title_impression: numeric_impressions[idx] if idx is not None and idx < len(numeric_impressions) else 0,
                    })
                    current_date -= timedelta(days=1)

                self.rows.append({
                    "title": self.platform,
                    "value": value_a,
                    "index": sheet_index,
                    "data": label_objects
                })

            self.total_rows = len(self.rows)
            return self

        except HttpError as error:
            print(f"An error occurred while reading sheet: {error}")
            self.currency = []
            self.rows = []
            self.total_rows = 0
            return self
