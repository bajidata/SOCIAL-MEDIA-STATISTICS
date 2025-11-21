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
        self.followers = None
        self.engagement = None
        self.impressions = None
        
        # Store data inside self
        self.currency = []        # all values in column A
        self.rows = []
        self.statistic = []            # row objects with index + value
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
        suspended_value = ["PKR"]
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
            # print(normalized)
            self.currency = []
            self.rows = []
            TITLE_MAP = {
                "TOTAL FOLLOWERS": "total_followers",
                "MONTHLY ENGAGEMENTS": "total_engagements",
                "MONTHLY IMPRESSIONS": "total_impressions",
            }

            today = datetime.strptime(self.yesterday_date, "%d-%m-%Y")

            for i, row in enumerate(normalized):

                value_a = row[0].strip()
                if value_a == "" or value_a.upper() in suspended_value:
                    continue

                self.currency.append(value_a)
                sheet_index = i + 1

                # row[1] = title of followers row
                raw_title_followers = row[1].strip()

                # Get engagement row (3 rows below)
                if i + 3 >= len(normalized):
                    continue

                engagement_row = normalized[i + 3]
                raw_title_engagement = engagement_row[1].strip()

                if i + 6 >= len(normalized):
                    continue

                impression_row = normalized[i + 6]
                raw_title_impression = impression_row[1].strip()

                # --- MAP TITLES ---
                title_followers = TITLE_MAP.get(raw_title_followers.upper(), raw_title_followers.lower().replace(" ", "_"))
                title_engagement = TITLE_MAP.get(raw_title_engagement.upper(), raw_title_engagement.lower().replace(" ", "_"))
                title_impression = TITLE_MAP.get(raw_title_impression.upper(), raw_title_impression.lower().replace(" ", "_"))


                # --- NUMERIC VALUES ---

                # Followers (row i)
                numeric_followers = []
                for val in row[2:]:
                    val = val.strip()
                    if val == "":
                        continue
                    numeric_followers.append(int(val))

                # Monthly Engagement
                numeric_engagements = []
                for val in engagement_row[3:]:  
                    val = val.strip()
                    if val == "":
                        continue
                    numeric_engagements.append(int(val))

                # Monthly Impression
                numeric_impression = []
                for val in impression_row[3:]:  
                    val = val.strip()
                    if val == "":
                        continue
                    numeric_impression.append(int(val))

                # Ensure equal lengths
                length = min(len(numeric_followers), len(numeric_engagements), len(numeric_impression))

                # --- MERGE INTO LABEL OBJECTS ---
                label_objects = []
                current_date = today

                for idx in range(length):
                    label_objects.append({
                        "date": current_date.strftime("%d/%m/%Y"),
                        title_followers: numeric_followers[idx],
                        title_engagement: numeric_engagements[idx],
                        title_impression: numeric_impression[idx]
                    })
                    current_date -= timedelta(days=1)
                    
                

                # Store
                self.rows.append({
                    "title": self.platform,
                    "value": value_a,
                    "index": sheet_index,
                    "data": label_objects
                })

            self.total_rows = len(self.rows)
            yesterday_formatted = datetime.strptime(self.yesterday_date, "%d-%m-%Y").strftime("%d/%m/%Y")
            # Get the date before yesterday
            day_before_yesterday = datetime.strptime(self.yesterday_date, "%d-%m-%Y") - timedelta(days=1)
            day_before_formatted = day_before_yesterday.strftime("%d/%m/%Y")

            if self.range == "Monthly":
                for platform in self.rows:
                    for entry in platform['data']:
                        if entry['date'] == yesterday_formatted:
                            self.statistic.append({
                                "platform": platform['title'],
                                "Range": self.range,
                                "value": platform['value'],
                                "date": entry['date'],
                                "followers": entry['total_followers'],
                                "engagements": entry['total_engagements'],
                                "impressions": entry['total_impressions']
                            })
                            break
            
            if self.range == "Daily":
                for platform in self.rows:
                    yesterday_data = None
                    day_before_data = None

                    for entry in platform['data']:
                        if entry['date'] == yesterday_formatted:
                            yesterday_data = entry
                        elif entry['date'] == day_before_formatted:
                            day_before_data = entry

                    if yesterday_data and day_before_data:
                        # Get values
                        y_followers = yesterday_data['total_followers']
                        y_engagements = yesterday_data['total_engagements']
                        y_impressions = yesterday_data['total_impressions']

                        prev_followers = day_before_data['total_followers']
                        prev_engagements = day_before_data['total_engagements']
                        prev_impressions = day_before_data['total_impressions']

                        # Calculate daily difference
                        followers_diff = y_followers - prev_followers
                        engagement_diff = y_engagements - prev_engagements
                        impressions_diff = y_impressions - prev_impressions

                        # Append statistic
                        self.statistic.append({
                            "platform": platform['title'],
                            "Range": self.range,
                            "value": platform['value'],
                            "date": f"{yesterday_formatted} - {day_before_formatted}",
                            "followers": followers_diff,
                            "engagements": engagement_diff,
                            "impressions": impressions_diff
                        })
            if self.range == "Weekly":
                for platform in self.rows:
                    # Collect data for the last 7 days
                    weekly_entries = []
                    for entry in platform['data']:
                        entry_date = datetime.strptime(entry['date'], "%d/%m/%Y")
                        yesterday_dt = datetime.strptime(self.yesterday_date, "%d-%m-%Y")
                        if 0 <= (yesterday_dt - entry_date).days < 7:
                            weekly_entries.append(entry)

                    if len(weekly_entries) >= 2:
                        # Sort entries by date ascending (oldest first)
                        weekly_entries.sort(key=lambda x: datetime.strptime(x['date'], "%d/%m/%Y"))

                        first_day = weekly_entries[0]
                        last_day = weekly_entries[-1]

                        # Calculate difference between last day (yesterday) and first day (6 days before)
                        followers_diff = last_day['total_followers'] - first_day['total_followers']
                        engagement_diff = last_day['total_engagements'] - first_day['total_engagements']
                        impressions_diff = last_day['total_impressions'] - first_day['total_impressions']

                        # Append weekly statistic
                        self.statistic.append({
                            "platform": platform['title'],
                            "Range": self.range,
                            "value": platform['value'],
                            "date": f"{first_day['date']} - {last_day['date']}",
                            "followers": followers_diff,
                            "engagements": engagement_diff,
                            "impressions": impressions_diff
                        })
            return self

        except HttpError as error:
            print(f"An error occurred while reading sheet: {error}")
            self.currency = []
            self.rows = []
            self.total_rows = 0
            return self
