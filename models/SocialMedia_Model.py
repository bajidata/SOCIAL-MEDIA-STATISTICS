class SocialMedia_Model:
    def __init__(self, platform, brand, date):
        self.platform = platform
        self.brand = brand
        self.date = date
        self.followers = 10000
        self.engagement = 12212
        self.impressions = 343443
    
    def analytics(self):
        """Simulates getting data from a database"""
        # we should process the sheet collection here
        return self