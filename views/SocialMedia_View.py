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
                # "timeframe": model.range,
                "row": model.rows,
                "column_a": model.currency,
                "length": model.total_rows
            },
            "statistics": {
                "data": model.statistic
            }
        }