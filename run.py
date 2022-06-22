import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')

def get_sales_data():
    """
    Get sales figures input from the user 
    """
    while True:
        print('Please enter the sales data from the last market.')
        print('Data should be six numbers, separated by commas.')
        print('Example: 10,20,30,40,50,60\n')
        data_str = input('Enter your data here:\n ')
    
        sales_data = data_str.split(',')
        
        if validate_data(sales_data):
            print('Data is valid!')
            break

    return sales_data
def validate_data(values):
    """
    Inside the try, converts all string values into integers.
    Raises ValueError if strings cannot be converted into int,
    or if there aren't exactly 6 values.
    """
    print(values)
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values required, you provide {len(values)} "
            ) 
    except ValueError as e:
        print(f"Invalide data: {e}, please try again.\n")
        return False
    return True


def update_worksheet(data, worksheet):
    print(f"Updating {worksheet} worksheet...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} updated succesfully.\n")

def calculate_surplus_data(sales_row):
    """
    compare sales with stock values to get the surplus value.

    if number is positive indicate waste, if negative stock sold out
    """

    print("Calculating surplus data...\n")
    stock = SHEET.worksheet('stock').get_all_values()
    stock_row = stock.pop()

    surplus_data = []
    for sales, stock in zip(sales_row, stock_row):
        surplus = int(stock) - int(sales)
        surplus_data.append(surplus)
    
    return surplus_data


def get_last_5_entires_sales():
    """
    collect the last 5 values of every coloumn to calculate the stock for the next day
    """
    sales = SHEET.worksheet('sales')

   
    coloumns = []
    for ind in range(1,7):
        coloumn = sales.col_values(ind)
        coloumns.append(coloumn[-5:])
    return coloumns

def calculate_stock_data(data):
    """
    Calculate the stock data
    """
    print("Calculate stock data...\n")
    new_stock_data = []
    for coloumn in data:
        int_coloumn = [int(num) for num in coloumn]
        average = (sum(int_coloumn) / len(int_coloumn))
        stock_num = average *1.1
        new_stock_data.append(round(stock_num))        

    return new_stock_data


def main():
    """
    Run all program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, 'sales')
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, 'surplus')
    sales_coloumns = get_last_5_entires_sales()
    stock_data = calculate_stock_data(sales_coloumns)
    update_worksheet(stock_data, 'stock')
print("Welcome to Love Sandwiches data Automation")
main()
