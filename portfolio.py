
import csv
import yfinance as yf
from datetime import datetime
import os


# Store all stock details
portfolio = {}


def get_stock_price(symbol):
    """Fetch the latest available stock price."""

    try:
        stock = yf.Ticker(symbol)

        # Try to get the latest available price
        stock_info = stock.fast_info
        current_price = stock_info.get("last_price")

        if current_price is not None and current_price > 0:
            return float(current_price)

        # Try historical market data if fast_info is unavailable
        history = stock.history(period="5d")

        if not history.empty:
            current_price = float(history["Close"].dropna().iloc[-1])

            if current_price > 0:
                return current_price

        raise ValueError("Stock price not available.")

    except Exception as error:
        raise ValueError(
            f"Could not retrieve price for {symbol}: {error}"
        )


def get_positive_number(message):
    """Accept only positive numeric values."""

    while True:
        try:
            value = float(input(message))

            if value <= 0:
                print("Please enter a value greater than zero.")
            else:
                return value

        except ValueError:
            print("Invalid input. Please enter a valid number.")


def add_stocks():
    """Collect stock details from the user."""

    print("\n--- Enter Your Stock Details ---")
    print("Type DONE when you finish adding stocks.")

    while True:
        symbol = input("\nEnter stock ticker: ").strip().upper()

        if symbol == "DONE":
            break

        if not symbol:
            print("Ticker cannot be empty.")
            continue

        if symbol in portfolio:
            print("This stock is already added.")
            continue

        buy_price = get_positive_number("Enter buying price: ")

        quantity = get_positive_number("Enter number of shares: ")

        if not quantity.is_integer():
            print("Please enter a whole number of shares.")
            continue

        portfolio[symbol] = {
            "buy_price": buy_price,
            "quantity": int(quantity)
        }

        print(f"{symbol} added successfully!")


def calculate_portfolio():
    """Calculate investment and current portfolio values."""

    results = []

    total_invested = 0
    total_current_value = 0

    print("\n" + "=" * 90)
    print("             STOCK PORTFOLIO PERFORMANCE REPORT")
    print("=" * 90)

    print(
        f"{'Ticker':<12}"
        f"{'Quantity':<10}"
        f"{'Buy Price':>13}"
        f"{'Current Price':>16}"
        f"{'Invested':>14}"
        f"{'Current Value':>17}"
        f"{'Profit/Loss':>15}"
    )

    print("-" * 90)

    for symbol, details in portfolio.items():

        try:
            buy_price = details["buy_price"]
            quantity = details["quantity"]

            current_price = get_stock_price(symbol)

            invested_amount = buy_price * quantity
            current_value = current_price * quantity

            profit_loss = current_value - invested_amount

            if invested_amount > 0:
                profit_percentage = (
                    profit_loss / invested_amount
                ) * 100
            else:
                profit_percentage = 0

            total_invested += invested_amount
            total_current_value += current_value

            results.append({
                "ticker": symbol,
                "quantity": quantity,
                "buy_price": buy_price,
                "current_price": current_price,
                "invested_amount": invested_amount,
                "current_value": current_value,
                "profit_loss": profit_loss,
                "profit_loss_percent": profit_percentage
            })

            print(
                f"{symbol:<12}"
                f"{quantity:<10}"
                f"{buy_price:>13.2f}"
                f"{current_price:>16.2f}"
                f"{invested_amount:>14.2f}"
                f"{current_value:>17.2f}"
                f"{profit_loss:>15.2f}"
            )

        except ValueError as error:
            print(f"\n{error}")
            return

    total_profit_loss = total_current_value - total_invested

    if total_invested > 0:
        total_percentage = (
            total_profit_loss / total_invested
        ) * 100
    else:
        total_percentage = 0

    print("-" * 90)
    print(f"Total Investment : {total_invested:.2f}")
    print(f"Current Value    : {total_current_value:.2f}")
    print(f"Total Profit/Loss: {total_profit_loss:.2f}")
    print(f"Overall Return   : {total_percentage:.2f}%")

    save_to_csv(
        results,
        total_invested,
        total_current_value,
        total_profit_loss,
        total_percentage
    )


def save_to_csv(results, total_invested,
                total_current_value, total_profit_loss,
                total_percentage):
    """Save portfolio performance into a CSV file."""

    filename = "portfolio_summary.csv"

    file_exists = os.path.exists(filename)

    fieldnames = [
        "date_time",
        "record_type",
        "ticker",
        "quantity",
        "buy_price",
        "current_price",
        "invested_amount",
        "current_value",
        "profit_loss",
        "profit_loss_percent"
    ]

    current_time = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    try:
        with open(
            filename,
            mode="a",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.DictWriter(
                file,
                fieldnames=fieldnames
            )

            if not file_exists or os.path.getsize(filename) == 0:
                writer.writeheader()

            for result in results:
                row = {
                    "date_time": current_time,
                    "record_type": "HOLDING",
                    **result
                }

                writer.writerow(row)

            writer.writerow({
                "date_time": current_time,
                "record_type": "PORTFOLIO TOTAL",
                "ticker": "TOTAL",
                "quantity": "",
                "buy_price": "",
                "current_price": "",
                "invested_amount": total_invested,
                "current_value": total_current_value,
                "profit_loss": total_profit_loss,
                "profit_loss_percent": total_percentage
            })

        print(f"\nPortfolio saved successfully to {filename}")

    except OSError as error:
        print(f"Error saving CSV file: {error}")


def main():
    """Main function to run the application."""

    print("=" * 50)
    print("       STOCK PORTFOLIO TRACKER")
    print("=" * 50)

    print("Enter your stock details below.")

    add_stocks()

    if not portfolio:
        print("\nNo stocks were entered.")
        return

    calculate_portfolio()


# Start the program
if __name__ == "__main__":
    main()
