import yfinance as yf


class StockPortfolio:
    def _init_(self):
        self.portfolio = {}

    def add_stock(self, symbol, shares):
        """Adds a stock to the portfolio."""
        if symbol in self.portfolio:
            self.portfolio[symbol] += shares
        else:
            self.portfolio[symbol] = shares
        print(f"\n✅ Successfully added {shares} shares of {symbol} to your portfolio!")

    def remove_stock(self, symbol, shares):
        """Removes shares of a stock from the portfolio."""
        if symbol in self.portfolio:
            if shares >= self.portfolio[symbol]:
                del self.portfolio[symbol]
                print(f"\n❌ Removed {symbol} completely from your portfolio.")
            else:
                self.portfolio[symbol] -= shares
                print(f"\n🗑️ Removed {shares} shares of {symbol} from your portfolio.")
        else:
            print(f"\n⚠️ {symbol} is not in your portfolio.")

    def get_portfolio_value(self):
        """Returns the total value of the portfolio."""
        total_value = 0
        print("\n📊 --- Portfolio Overview --- 📊")

        if not self.portfolio:
            print("Your portfolio is currently empty.")
            return total_value

        for symbol, shares in self.portfolio.items():
            stock = yf.Ticker(symbol)
            stock_data = stock.history(period="1d")

            # Check if any data was returned
            if stock_data.empty:
                print(f"⚠️  No data found for {symbol}. It might be delisted or unavailable.")
                continue

            try:
                # Use .iloc[0] to access the first row safely
                stock_price = stock_data['Close'].iloc[0]
                stock_value = stock_price * shares
                total_value += stock_value
                print(f"📈 {symbol}: {shares} shares @ ${stock_price:.2f} = ${stock_value:.2f}")
            except IndexError:
                print(f"⚠️  Could not retrieve price data for {symbol}.")

        print(f"\n💼 Total Portfolio Value: ${total_value:.2f}")
        return total_value


def main():
    portfolio = StockPortfolio()

    print("\n💰 Welcome to the Stock Portfolio Tracker! 💰")

    while True:
        print("\n--- 📈 Main Menu 📈 ---")
        print("1. ➕ Add Stock")
        print("2. ➖ Remove Stock")
        print("3. 💼 View Portfolio Value")
        print("4. ❌ Exit")

        choice = input("Please enter your choice (1-4): ")

        if choice == '1':
            symbol = input("\nEnter the stock symbol (e.g., AAPL): ").upper()
            try:
                shares = int(input(f"How many shares of {symbol} would you like to add? "))
                portfolio.add_stock(symbol, shares)
            except ValueError:
                print("⚠️ Invalid input! Please enter a valid number of shares.")

        elif choice == '2':
            symbol = input("\nEnter the stock symbol to remove (e.g., AAPL): ").upper()
            try:
                shares = int(input(f"How many shares of {symbol} would you like to remove? "))
                portfolio.remove_stock(symbol, shares)
            except ValueError:
                print("⚠️ Invalid input! Please enter a valid number of shares.")

        elif choice == '3':
            portfolio.get_portfolio_value()

        elif choice == '4':
            print("\n👋 Thank you for using the Stock Portfolio Tracker. Goodbye!")
            break

        else:
            print("⚠️ Invalid choice! Please select a valid option.")


if _name_ == "_main_":
    main()