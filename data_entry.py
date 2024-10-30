from datetime import datetime

#initialized the format for dates and category types
date_format = '%d-%m-%Y'
CATEGORIES = {'I':'Income','E':'Expense'}

#gets date from user and checks if its in valid format
def get_date(prompt, allow_default=False):
    date_str = input(prompt)
    if allow_default and not date_str:
        return datetime.today().strftime(date_format)
    
    try:
        valid_date = datetime.strptime(date_str, date_format)
        return valid_date.strftime(date_format)
    except ValueError:
        print('Invalid date format. Enter date as dd-mm-yyyy')
        return get_date(prompt, allow_default)

#gets amount of transaction   
def get_amount():
    while True:
        amount = float(input('Enter an amount: '))
        if amount <= 0:
            print()
            print('Amount must be non-negative and non-zero')
            continue
        else:
            break
    return amount
        
#gets category and checks if valid 
def get_category():
    while True:
        category = input("Enter category ('I' for Income or 'E' for Expense): ").upper()
        if category not in CATEGORIES:
            print("Invalid category. Enter 'I' for Income or 'E' for Expense")
        else:
            break  
    return CATEGORIES[category]
        
        
#gets description
def get_description():
    return input("Enter description: ")