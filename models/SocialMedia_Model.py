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
        self.platform = platform.lower()
        self.brand = brand.lower()
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
                "DAILY FOLLOWERS GAIN": "daily_followers_gain",
                "MONTHLY ENGAGEMENTS": "monthly_engagements",
                "DAILY ENGAGEMENTS": "daily_engagements",
                "MONTHLY IMPRESSIONS": "monthly_impressions",
                "DAILY IMPRESSIONS": "daily_impressions"
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
                if i + 1 >= len(normalized):
                    continue
                daily_followers_gain_row = normalized[i + 1]
                raw_title_daily_followers = daily_followers_gain_row[1].strip()



                # Get engagement row (3 rows below)
                if i + 3 >= len(normalized):
                    continue
                engagement_row = normalized[i + 3]
                raw_title_engagement = engagement_row[1].strip()

                if i + 2 >= len(normalized):
                    continue
                daily_engagement_row = normalized[i + 2]
                raw_title_daily_engagement = daily_engagement_row[1].strip()


                if i + 6 >= len(normalized):
                    continue
                impression_row = normalized[i + 6]
                raw_title_impression = impression_row[1].strip()

                if i + 5 >= len(normalized):
                    continue
                daily_impression_row = normalized[i + 5]
                raw_title_daily_impression = daily_impression_row[1].strip()

                # --- MAP TITLES ---
                title_followers = TITLE_MAP.get(raw_title_followers)
                title_daily_followers = TITLE_MAP.get(raw_title_daily_followers)
                title_engagement = TITLE_MAP.get(raw_title_engagement)
                title_daily_engagement = TITLE_MAP.get(raw_title_daily_engagement)
                title_impression = TITLE_MAP.get(raw_title_impression)
                title_daily_impression = TITLE_MAP.get(raw_title_daily_impression)



                # --- NUMERIC VALUES ---

                # Followers (row i)
                numeric_followers = []
                for val in row[2:]:
                    val = val.strip()
                    if val == "":
                        continue
                    numeric_followers.append(int(val))
                
                numeric_daily_followers_gain = []
                for val in daily_followers_gain_row[2:]:
                    val = val.strip()
                    if val == "":
                        continue
                    numeric_daily_followers_gain.append(int(val))

                # Monthly Engagement
                numeric_engagements = []
                for val in engagement_row[3:]:  
                    val = val.strip()
                    if val == "":
                        continue
                    numeric_engagements.append(int(val))

                # Daily Engagement
                numeric_daily_engagements = []
                for val in daily_engagement_row[2:]:  
                    val = val.strip()
                    if val == "":
                        continue
                    numeric_daily_engagements.append(int(val))

                # Monthly Impression
                numeric_impression = []
                for val in impression_row[3:]:  
                    val = val.strip()
                    if val == "":
                        continue
                    numeric_impression.append(int(val))
                
                numeric_daily_impression = []
                for val in daily_impression_row[2:]:  
                    val = val.strip()
                    if val == "":
                        continue
                    numeric_daily_impression.append(int(val))

                # Ensure equal lengths
                length = min(
                    len(numeric_followers), 
                    len(numeric_daily_followers_gain), 
                    len(numeric_engagements), 
                    len(numeric_daily_engagements), 
                    len(numeric_impression), 
                    len(numeric_daily_impression)
                )

                # --- MERGE INTO LABEL OBJECTS ---
                label_objects = []
                current_date = today

                for idx in range(length):
                    label_objects.append({
                        "date": current_date.strftime("%d/%m/%Y"),
                        title_followers: numeric_followers[idx],
                        title_daily_followers: numeric_daily_followers_gain[idx],
                        title_daily_engagement: numeric_daily_engagements[idx],
                        title_engagement: numeric_engagements[idx],
                        title_daily_impression: numeric_daily_impression[idx],
                        title_impression: numeric_impression[idx],                        
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

            if self.range == "monthly":
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
            
            if self.range == "daily":
                for platform in self.rows:
                    yesterday_entry = None

                    for entry in platform['data']:
                        if entry['date'] == yesterday_formatted:
                            yesterday_entry = entry
                            break

                    if yesterday_entry:
                        self.statistic.append({
                            "platform": platform['title'],
                            "Range": self.range,
                            "value": platform['value'],
                            "date": yesterday_formatted,
                            "followers": yesterday_entry.get("daily_followers_gain", 0),
                            "engagements": yesterday_entry.get("daily_engagements", 0),
                            "impressions": yesterday_entry.get("daily_impressions", 0)
                        })
            if self.range == "weekly":
                for platform in self.rows:

                    # Collect daily entries for last 7 days
                    weekly_entries = []
                    yesterday_dt = datetime.strptime(self.yesterday_date, "%d-%m-%Y")

                    for entry in platform['data']:
                        entry_date = datetime.strptime(entry['date'], "%d/%m/%Y")
                        diff = (yesterday_dt - entry_date).days

                        if 0 <= diff < 7:     # only last 7 days
                            weekly_entries.append(entry)

                    # Must have at least 1 day
                    if weekly_entries:
                        # Sum daily values
                        total_followers = sum(e.get('daily_followers_gain', 0) for e in weekly_entries)
                        total_engagements = sum(e.get('daily_engagements', 0) for e in weekly_entries)
                        total_impressions = sum(e.get('daily_impressions', 0) for e in weekly_entries)

                        # Get date range string
                        weekly_entries.sort(key=lambda x: datetime.strptime(x['date'], "%d/%m/%Y"))
                        first_day = weekly_entries[0]['date']
                        last_day = weekly_entries[-1]['date']

                        # Append result
                        self.statistic.append({
                            "platform": platform['title'],
                            "Range": self.range,
                            "value": platform['value'],
                            "date": f"{first_day} - {last_day}",
                            "followers": total_followers,
                            "engagements": total_engagements,
                            "impressions": total_impressions
                        })

            return self

        except HttpError as error:
            print(f"An error occurred while reading sheet: {error}")
            self.currency = []
            self.rows = []
            self.total_rows = 0
            return self
