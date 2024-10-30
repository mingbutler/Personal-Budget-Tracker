import pandas as pd 
import csv
from datetime import datetime
from data_entry import get_date,get_amount,get_category,get_description
import matplotlib.pyplot as plt

class CSV:
    CSV_FILE = 'data.csv'
    COLUMNS = ['Date','Amount','Category','Description']
    FORMAT = '%d-%m-%Y'
    
    @classmethod
    #initializes csv file if not already created
    def initialize_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=cls.COLUMNS)
            df.to_csv(cls.CSV_FILE, index = False)
            
    @classmethod
    def add_entry(cls,date,amount,category,description):
        new_entry = {
            'Date': date,
            'Amount': amount,
            'Category': category,
            'Description':description
        }
        #writes to a new line to the file
        with open(cls.CSV_FILE,'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile,fieldnames=cls.COLUMNS)
            writer.writerow(new_entry)
            print('Entry added successfully')
            
        
    @classmethod
    def get_transactions(cls,start_date,end_date):
        df = pd.read_csv(cls.CSV_FILE) 
        #converts date to date object and formats the date      
        df["Date"] = pd.to_datetime(df["Date"],format=CSV.FORMAT)
        df = df.sort_values(by='Date')
        start_date = datetime.strptime(start_date,CSV.FORMAT)
        end_date = datetime.strptime(end_date,CSV.FORMAT)
        #creates filtered df with only the dates entered by user
        mask = (df["Date"] >= start_date) & (df['Date'] <= end_date)
        filtered_df = df.loc[mask]
        
        if filtered_df.empty:
            print('No transactions found')
        else:
            print(f"Transactions from {start_date.strftime(CSV.FORMAT)} to {end_date.strftime(CSV.FORMAT)}")
            print(filtered_df.to_string(index=False,formatters={'Date': lambda date: date.strftime(CSV.FORMAT)}))
            #sums the categories named income and expense
            total_income = filtered_df[filtered_df['Category'] == 'Income']['Amount'].sum()
            total_expense = filtered_df[filtered_df['Category'] == 'Expense']['Amount'].sum()
            savings = total_income - total_expense
            print("\n--Summary--")
            print(f"Total Income: ${total_income:.2f}")
            print(f"Total Expense: ${total_expense:.2f}")
            print(f"Net Savings: ${savings:.2f}")
            
        return filtered_df
            
#adds entry to file       
def add():
    CSV.initialize_csv()
    date = get_date("Enter the date of the transaction (mm-dd-yyyy) or ENTER for today's date:",allow_default=True)
    amount = get_amount()
    category = get_category()
    description = get_description()
    CSV.add_entry(date,amount,category,description)

#prints all data
def show_all(budget):
    df = pd.read_csv(CSV.CSV_FILE)
    print(df.to_string(index=False))
    total_income = df[df['Category']=='Income']['Amount'].sum()
    total_expense = df[df['Category']=='Expense']['Amount'].sum()
    savings = total_income - total_expense
    if budget>0:
        print("\n--Summary--")
        print(f"Budget: ${budget:.2f}")
        print(f"Total Income: ${total_income:.2f}")
        print(f"Total Expense: ${total_expense:.2f}")
        set_budget(budget)
    else:
        print("\n--Summary--")
        print(f"Total Income: ${total_income:.2f}")
        print(f"Total Expense: ${total_expense:.2f}")
        print(f"Net Savings: ${savings:.2f}")
            
#plots data by date
def plot_transactions(df):
    df.set_index('Date',inplace=True)
    
    income_df = df[df['Category']=='Income'].resample('D').sum().reindex(df.index,fill_value=0)
    expense_df = df[df['Category']=='Expense'].resample('D').sum().reindex(df.index,fill_value=0)
    
    plt.figure(figsize=(10,5))
    plt.plot(income_df.index,income_df['Amount'],label='Income',color='g')
    plt.plot(expense_df.index,expense_df['Amount'],label='Expense',color='r')
    plt.xlabel='Date'
    plt.ylabel='Amount'
    plt.title('Income and Expenses Summary')
    plt.legend()
    plt.grid(True)
    plt.show()
  
#plots all data
def plot_full_transactions():
    df = pd.read_csv(CSV.CSV_FILE)       
    df["Date"] = pd.to_datetime(df["Date"],format=CSV.FORMAT)
    df = df.sort_values(by='Date')
    df.set_index('Date',inplace=True)
    
    income_df = df[df['Category']=='Income'].resample('D').sum().reindex(df.index,fill_value=0)
    expense_df = df[df['Category']=='Expense'].resample('D').sum().reindex(df.index,fill_value=0)
    
    plt.figure(figsize=(10,5))
    plt.plot(income_df.index,income_df['Amount'],label='Income',color='g')
    plt.plot(expense_df.index,expense_df['Amount'],label='Expense',color='r')
    plt.xlabel='Date'
    plt.ylabel='Amount'
    plt.title('Income and Expenses Summary')
    plt.legend()
    plt.grid(True)
    plt.show()
    
#clears file keeping columns
def clear():
    with open(CSV.CSV_FILE,'r+') as csvfile:
        csvfile.readline()
        csvfile.truncate(csvfile.tell())
    
#sets budget and calculates remaining budget after each transaction   
def set_budget(budget):
    df = pd.read_csv(CSV.CSV_FILE)
    total_expense = df[df['Category'] == 'Expense']['Amount'].sum()
    budget_left = budget - total_expense
    print(f"Budget remaining: ${budget_left:.2f}")
    
    
         
def main():
    print()
    print('Welcome to your budget tracker!')
    budget_choice = input('Do you want to set a budget? (y/n) ').lower()
    if budget_choice=='y':
        while True:
            budget = float(input('Enter budget: '))
            if budget<0:
                print()
                print('Please enter valid amount')
    
    while(True):
        print()
        print("Click ENTER to view full transaction summary")
        print('1) Add transaction')
        print("2) View transaction summary within date range")
        print("3) Start a new month")
        print("q) to exit")
        choice = input("Enter choice: ")
        
        if choice == '':
            show_all(budget)
            if input("Would you like to see a graph? (y/n) ").lower()=='y':
                plot_full_transactions()
            
        elif(choice == '1'):
            add()
        elif(choice == '2'):
            start = get_date("Enter start date (dd-mm-yyyy): ")
            end = get_date("Enter end date (dd-mm-yyyy): ")
            df = CSV.get_transactions(start,end)
            if input("Would you like to see a graph? (y/n) ").lower()=='y':
                plot_transactions(df)
        elif(choice == '3'):
            clear()
        elif(choice == 'q'):
            print("Exiting...")
            break
        else:
            print("Invalid option")
            

if __name__ == "__main__":
    main()
    
    
    
  
#random file entries for testing 
'''
Date,Amount,Category,Description
28-09-2024,57.79,Expense,amazon
28-09-2024,300.34,Expense,grocery
30-09-2024,50.00,Expense,lunch
01-10-2024,250.00,Expense,grocery
02-10-2024,1500.00,Expense,rent
02-10-2024,2500.00,Income,paycheck
04-10-2024,20.00,Expense,Movie ticket
04-10-2024,15.00,Expense,coffee
05-10-2024,30.00,Expense,Uber
06-10-2024,300.00,Expense,shopping
07-10-2024,117.00,Expense,Dinner
08-10-2024,10.00,Expense,Netflix subscription
09-10-2024,50.00,Expense,Electric bill
10-10-2024,2500.00,Income,paycheck
11-10-2024,100.00,Income,sold clothes
12-10-2024,25.00,Expense,Shopping
14-10-2024,5.00,Expense,Parking meter
14-10-2024,60.00,Expense,Concert tickets
15-10-2024,300.00,Expense,grocery
17-10-2024,2500.00,Income,paycheck
20-10-2024,25.00,Expense,amazon
24-10-2024,2500.00,Income,paycheck
28-10-2024,1000.00,Expense,retirement22-10-2024
22-10-2024,5.0,Expense,amazon
22-10-2024,20.0,Expense,amazon
'''