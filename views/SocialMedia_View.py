def filter_data():
    platform = input("Enter Platform: ")
    brand = input("Enter Brand: ")
    date = input("Date (Daily, Weekly, Monthly): ")
    return platform, brand, date

def show_data(model):
    print("This is your inputted Data")
    print(model.platform)
    print(model.brand)
    print(model.date)