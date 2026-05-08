import csv
import matplotlib.pyplot as plt

print("=== TRADING FRAMEWORK v7 (EXCEL EXPORT) ===\n")

FILE_NAME = "trades.csv"
EXPORT_FILE = "trades_export.csv"

trades = []

# Load trades
try:
    with open(FILE_NAME, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            trades.append(float(row[0]))
except FileNotFoundError:
    pass


def save_trade(pnl):
    with open(FILE_NAME, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([pnl])


def export_to_excel():
    with open(EXPORT_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Trade #", "PnL", "Cumulative Equity"])

        equity = 0
        for i, t in enumerate(trades, start=1):
            equity += t
            writer.writerow([i, t, equity])

    print("Exported to Excel file:", EXPORT_FILE)


def show_equity_curve():
    equity = []
    balance = 0

    for t in trades:
        balance += t
        equity.append(balance)

    plt.plot(equity)
    plt.title("Equity Curve")
    plt.xlabel("Trades")
    plt.ylabel("Balance")
    plt.grid(True)
    plt.show()


while True:
    print("\n1. Add trade")
    print("2. Show analytics")
    print("3. Show equity curve")
    print("4. Export to Excel")
    print("5. Exit")

    choice = input("Choose option: ")

    if choice == "1":
        pnl = float(input("Enter PnL ($): "))
        trades.append(pnl)
        save_trade(pnl)
        print("Trade saved.")

    elif choice == "2":
        total = len(trades)
        wins = len([t for t in trades if t > 0])
        losses = len([t for t in trades if t <= 0])

        total_pnl = sum(trades)
        win_rate = (wins / total * 100) if total > 0 else 0

        print("\n--- ANALYTICS ---")
        print("Total Trades:", total)
        print("Wins:", wins)
        print("Losses:", losses)
        print("Win Rate:", round(win_rate, 2), "%")
        print("Total PnL: $", round(total_pnl, 2))

    elif choice == "3":
        show_equity_curve()

    elif choice == "4":
        export_to_excel()

    elif choice == "5":
        break