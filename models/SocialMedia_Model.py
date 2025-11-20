from config.loader import (
    TYPE, PROJECT_ID, PRIVATE_KEY_ID, PRIVATE_KEY, CLIENT_EMAIL, CLIENT_ID,
    AUTH_URI, TOKEN_URI, AUTH_PROVIDER_X509_CERT_URL, CLIENT_X509_CERT_URL, UNIVERSE_DOMAIN,
    TESTING_SHEET_ID
)
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.service_account import Credentials
from calendar import monthrange
from datetime import datetime, timedelta


class SocialMedia_Model:
    def __init__(self, platform, brand, yesterday_date, range):
        self.platform = platform
        self.brand = brand.upper()
        self.yesterday_date = yesterday_date
        self.range = range
        self.followers = 10001
        self.engagement = 12212
        self.impressions = 343443

        # Store data inside self
        self.currency = []        # all values in column A
        self.rows = []            # row objects with index + value
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
        n+=2
        original = n
        while n > 0:
            n, remainder = divmod(n - 1, 26)
            result = chr(65 + remainder) + result

        # print(n)
        print(original)
        return result, original

    def analytics(self):
        """Fetch Columns A:V, map B-V rows with title first, then descending date-value objects"""
        
        sheet_id = TESTING_SHEET_ID
        today = datetime.strptime(self.yesterday_date, "%d-%m-%Y")
        days_in_month = monthrange(today.year, today.month)[1]  # 28–31
        last_day_letter, corresponding_number = self.number_to_column(days_in_month + 1)  # +1 if first column is title

        range_a_v = f"{self.brand}!A:{last_day_letter}"  # columns A to V

        try:
            result = (
                self.service.spreadsheets()
                .values()
                .get(spreadsheetId=sheet_id, range=range_a_v)
                .execute()
            )

            raw = result.get("values", [])
            normalized = [(row + [""]*corresponding_number)[:corresponding_number] for row in raw]

            self.currency = []
            self.rows = []

            metrics_by_row = {}    # { "TOTAL FOLLOWERS": [...], "DAILY": [...], ... }
            row_indices = {}       # track sheet index for each metric row
            metric_titles = []     # preserve order

            today = datetime.strptime(self.yesterday_date, "%d-%m-%Y")

            for i, row in enumerate(normalized):

                value_a = row[0].strip()
                # print(value_a)
                if value_a == "":
                    continue

                self.currency.append(value_a)
                sheet_index = i + 1

                # Column B: title
                TITLE_MAP = {
                    "TOTAL FOLLOWERS": "total_followers",
                    "TOTAL ENGAGEMENT": "total_engagement",
                    "TOTAL IMPRESSIONS": "total_impressions"
                }

                raw_title = row[1].strip() if len(row) > 1 else ""
                # print(raw_title)

                # Remaining numeric values
                numeric_values = []
                for val in row[2:]:
                    val = val.strip()
                    if val == "":
                        continue
                    try:
                        numeric_values.append(int(val))
                    except ValueError:
                        numeric_values.append(val)

                # Build label array: first object is title
                # label_objects = [{"title": self.platform}]
                label_objects = []

                # Then append descending date-value objects for numeric values
                current_date = today
                for val in numeric_values:
                    title = TITLE_MAP.get(raw_title.upper(), raw_title.lower().replace(" ", "_"))
                    label_objects.append({
                        "date": current_date.strftime("%d/%m/%Y"),
                         title: val
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
