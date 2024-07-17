from datetime import datetime

date_format = "%d-%m-%Y"
CATEGORIES = {"I": "Income", "E": "Expense"}

def get_date(form_date):
    try:
        valid_date = datetime.strptime(form_date, date_format)
        return valid_date.strftime(date_format)
    except ValueError:
        print("Invalid date format. Please enter the date in dd-mm-yyyy format")

def get_amount(form_amount):
    try:
        if form_amount <= 0:
            raise ValueError("Amount must be a non-negative non-zero value.")
        return form_amount
    except ValueError as e:
        print(e)
        return get_amount()

def get_category():
    category = input("Enter the category ('I' for Income or 'E' for Expense): ").upper()
    if category in CATEGORIES:
        return CATEGORIES[category]
    
    print("Invalid category. 'I' for Income or 'E' for Expense")
    return get_category()

def get_description():
    return input("Enter a description (optional): ")
        