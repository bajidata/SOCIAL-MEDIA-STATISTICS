class SocialMediaView:

    def format_response(self, model):
        """
        Receives a Model Object -> Returns a Dictionary
        """
        return {
            "status": "success",
            "meta": {
                "platform_queried": model.platform,
                "brand_queried": model.brand,
                "yesterday": model.yesterday_date,
                "timeframe": model.date
            },
            "statistics": {
                "total_followers": model.followers,
                "total_engagements": model.engagement,
                "total_impressions": model.impressions
            }
        }