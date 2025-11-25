from models.SocialMedia_Model import SocialMedia_Model
from views.SocialMedia_View import SocialMediaView

class SocialMedia_Controller():
    def __init__(self):
        self.view = SocialMediaView()

    def process_stats(self, platform: str, brand: str, yesterday_date: str, range: str):
        # simulate input
        print("backend API Processing")
        # handle the request input
        if platform.lower() == "facebook":
            
            model = SocialMedia_Model(platform, brand, yesterday_date, range)# Passing the Variable as Parameters
            model.analytics() # The returning
        

        # Call the VIEW to format that model into a clean dictionary
        response_data = self.view.format_response(model)

        print("Backend Done Processing..")

        # Return the dictionary to the Router
        return response_data