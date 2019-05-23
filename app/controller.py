from app.account import Account
from app.position import Position
from app import views
from app import util

def main():
    while True:
        views.generic_msg("Welcome to Terminal Trader !")
        selection = views.welcome_menu()
        if selection is None: #Bad input
            views.generic_msg("Please enter a number that corresponds to a stated option")
        elif selection == 3: #Exit
            views.generic_msg("Bye: Thanks for using Terminal Trader")
            break
        elif selection == 1: #Create account
            new_username = views.get_input("Username")
            new_password = views.get_input("Password")            
            new_account = Account(username=new_username)
            new_account.set_password(new_password)
            new_account.save()
        elif selection == 2: #Login
            login_username = views.get_input("Username")
            login_password = views.get_input("Password")      
            if not Account.login(login_username, login_password):
                views.generic_msg("Failed to find an account for the given Username/Password, pls retry")
            else: #Store account pk for re-use
                pk = Account.login(login_username, login_password).pk
                while True:
                    choice = views.main_menu()
                    if choice is None: #Bad input
                        views.generic_msg("Please enter a number that corresponds \
                                           to a stated option")
                    elif choice == 8: #Exit
                        break
                    elif choice == 1: #View Balance & Positions
                        positions_sub_menu(pk)
                    elif choice == 2: #Deposit money
                        deposit_amount = float(views.get_input("Deposit Amount"))
                        account_deposit = Account(pk=pk)
                        new_bal = account_deposit.deposit(deposit_amount)
                        account_deposit.save()
                        views.generic_msg("New Balance = {}".format(new_bal))
                    elif choice == 3: #Look up stock price
                        ticker = views.get_input("Please enter a Ticker Symbol")
                        quote = util.get_price(ticker)
                        if not quote: 
                            views.generic_msg("The Ticker Symbol entered does not exist")
                        else:
                            views.stock_price(ticker, quote)
                    elif choice == 4: #Look up ticker from Co. name
                        co_name = views.get_input("Please enter Company Name")
                        companies = util.get_ticker(co_name )
                        if not companies: 
                            views.generic_msg("No matches for input Company Name")
                        else:
                            for co in companies:
                                views.show_companies(co) 
                    elif choice == 5: #Buy stock
                        ticker = views.get_input("Please enter a Ticker Symbol")
                        shares_buy = views.get_input("Please enter the number of shares to buy")
                        buy_txn = Account(pk=pk)
                        buy_txn.buy(ticker, shares_buy)
                        views.generic_msg("Buy transaction complete")                      
                    elif choice == 6: #Sell stock
                        ticker = views.get_input("Please enter a Ticker Symbol")
                        shares_sell = views.get_input("Please enter the number of shares to sell")
                        sell_txn = Account(pk=pk)
                        sell_txn.sell(ticker, shares_sell)
                        views.generic_msg("Sell transaction complete")  
                    elif choice == 7: #View Trade History
                        trades_sub_menu(pk)
        
def positions_sub_menu(pk):
    retrieve_bal = Account(pk=pk)
    views.generic_msg("Your current balance = {}".format(retrieve_bal.get_account().balance))
    while True:
        position_choice = views.position_menu()    
        if position_choice is None: #Bad input
            views.generic_msg("Please enter a number that corresponds to a stated option")
        elif position_choice == 3: #Exit
            break
        elif position_choice == 1: #Retrieve and display a given position
            ticker = views.get_input("Please enter a Ticker Symbol")
            user_position = Account(pk=pk)
            position = user_position.get_position_for(ticker)
            valuation = Position()  
            getval = valuation.current_value(ticker, position.shares)      
            views.show_positions(position, getval)
        elif position_choice == 2: #Retrieve and display all positions
            user_positions = Account(pk=pk)
            positions = user_positions.get_positions()
            for position in positions:
                valuation = Position()  
                getval = valuation.current_value(position.ticker, position.shares)     
                views.show_positions(position, getval)

def trades_sub_menu(pk):
    while True:
        trade_choice = views.trades_menu()    
        if trade_choice is None: #Bad input
            views.generic_msg("Please enter a number that corresponds to a stated option")
        elif trade_choice == 3: #Exit
            break
        elif trade_choice == 1: #Retrieve and display trades re a given ticker
            ticker = views.get_input("Please enter a Ticker Symbol")
            user_trades = Account(pk=pk)
            trades = user_trades.get_trades_for(ticker)
            for trade in trades:
                views.show_trades(trade)
        elif trade_choice == 2: #Retrieve and display all trades
            user_trades = Account(pk=pk)
            trades = user_trades.get_trades()
            for trade in trades:
                views.show_trades(trade) 

def run():
    main()


