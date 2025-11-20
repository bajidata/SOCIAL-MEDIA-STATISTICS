from datetime import date, timedelta, datetime

# Fixed test date
yesterday = datetime.strptime("11-09-2001", "%m-%d-%Y").date()
today = yesterday + timedelta(days=1)  # optional, just for first_day_of_month

first_day_of_month = yesterday.replace(day=1)

yesterday_date = yesterday.strftime("%m-%d-%Y")

# Weekly test
start_date = yesterday - timedelta(days=6)
start_date = max(start_date, first_day_of_month)

date_range = [
    (start_date + timedelta(days=i)).strftime("%m-%d-%Y")
    for i in range((yesterday - start_date).days + 1)
]

print("Yesterday:", yesterday_date)
print("Weekly date range:", date_range)
