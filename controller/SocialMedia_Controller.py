from models.SocialMedia_Model import SocialMedia_Model
from views.SocialMedia_View import filter_data, show_data

class SocialMedia_Controller():
    def __init__(self):
        self.model = None

    def run(self):
        platform, brand, date = filter_data()  # view handles input
        self.model = SocialMedia_Model(platform, brand, date)  # model stores data
        show_data(self.model)