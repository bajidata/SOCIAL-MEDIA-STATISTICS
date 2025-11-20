from config.loader import (
    TYPE, PROJECT_ID, PRIVATE_KEY_ID, PRIVATE_KEY, CLIENT_EMAIL, CLIENT_ID,
    AUTH_URI, TOKEN_URI, AUTH_PROVIDER_X509_CERT_URL, CLIENT_X509_CERT_URL, UNIVERSE_DOMAIN,
    TESTING_SHEET_ID
)
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.service_account import Credentials

class SocialMedia_Model:
    def __init__(self, platform, brand, yesterday_date, date):
        self.platform = platform
        self.brand = brand
        self.yesterday_date = yesterday_date
        self.date = date
        self.followers = 10001
        self.engagement = 12212
        self.impressions = 343443

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


    
    def analytics(self):
        """Simulates getting data from a database"""
        # we should process the sheet collection here
        sheet_id = TESTING_SHEET_ID
        sheet_name = "Sheet2"

        row_data = [
                self.platform,
                self.brand,
                self.yesterday_date,
                self.followers,
                self.engagement,
                self.impressions,
        ]

        body = {
            "values": [row_data]
        }
        result = (
                self.service.spreadsheets()
                .values()
                .append(
                    spreadsheetId=sheet_id,
                    range=f"{sheet_name}!A1",
                    valueInputOption="USER_ENTERED",
                    insertDataOption="INSERT_ROWS",
                    body=body,
                )
                .execute()
            )



        return self