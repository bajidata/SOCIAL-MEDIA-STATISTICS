from models.SocialMedia_Model import SocialMedia_Model
from views.SocialMedia_View import SocialMediaView

class SocialMedia_Controller():
    def __init__(self):
        self.view = SocialMediaView()

    def process_stats(self, platform: str, brand: str, date: str):
        # simulate input
        
        # handle the request input
        model = SocialMedia_Model(platform, brand, date)  #
        model.analytics()

        # Call the VIEW to format that model into a clean dictionary
        response_data = self.view.format_response(model)

        # Return the dictionary to the Router
        return response_data