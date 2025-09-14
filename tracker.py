import os
from datetime import datetime
import matplotlib.pyplot as plt   # for pie chart

EXPENSE_FILE = "expenses.txt" # my expenses are recorded here


if not os.path.exists(EXPENSE_FILE):
    with open(EXPENSE_FILE, "w") as f:
        pass


#---------------------------------To add Expenses in Txt file---------------------------------------------------------

def add_expense():
    category = input("Enter category (e.g., Food, Travel, Shopping): ").strip() # strip() removes the extra spaces
    amount = input("Enter amount: ").strip()
    date = input("Enter date (YYYY-MM-DD): ").strip()

    try:
        datetime.strptime(date, "%Y-%m-%d") # striptime() validate the entered time
    except ValueError:
        print("Invalid date format! Please use YYYY-MM-DD.")
        return

    with open(EXPENSE_FILE, "a") as f:   #open the expense txt file in append mode so the data entered on the end
        f.write(f"{category},{amount},{date}\n")  # write the xpns in format Cat, amt, date

    print("Expense added successfully! (Recorded in expenses.txt)")

#----------------------------------------------------------------------------------------------------------------------------

#------------------------To View the expenses------------------------------------------

def view_expenses():
    if not os.path.getsize(EXPENSE_FILE):
        print("No expenses recorded yet.")
        return

    expenses = {}

    with open(EXPENSE_FILE, "r") as f:
        for line in f:
            parts = line.strip().split(",") # ( Read each line nd splits by , )
            if len(parts) != 3: # Invalid lines are skipped
                continue
            category, amount, date = parts
            if category not in expenses:
                expenses[category] = []
            expenses[category].append((amount, date)) #group expense by Category

    print("\nExpenses:")
    for category, items in expenses.items():
        print(f"\n{category}:")
        for i, (amount, date) in enumerate(items, start=1):
            print(f"{i}. Amount: {amount} - Date: {date}")

#---------------------------------------------------------------------------


def monthly_summary():
    if not os.path.getsize(EXPENSE_FILE):
        print("No expenses recorded yet.")
        return

    month_year = input("Enter month and year (YYYY-MM): ").strip()
    try:
        datetime.strptime(month_year + "-01", "%Y-%m-%d")
    except ValueError:
        print("Invalid format! Please use YYYY-MM.")
        return

    total = 0
    category_totals = {}

    with open(EXPENSE_FILE, "r") as f:
        for line in f:
            parts = line.strip().split(",")
            if len(parts) != 3:
                continue
            category, amount, date = parts
            if date.startswith(month_year):
                try:
                    amount = float(amount)
                except ValueError:
                    continue  
                total += amount
                category_totals[category] = category_totals.get(category, 0) + amount

    print(f"\nMonthly Summary ({month_year}):")
    print(f"Total Expenses: {total}")
    print("By Category:")
    for category, amt in category_totals.items():
        print(f"{category}: {amt}")

    # --- Pie Chart Visualization ---
    if category_totals:
        labels = list(category_totals.keys())
        values = list(category_totals.values())

        plt.figure(figsize=(6, 6))
        plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
        plt.title(f"Expense Breakdown - {month_year}")
        plt.show()
    else:
        print("No expenses found for this month!")
#----------------------------------------------------------------------------

def main():
    while True:
        print("\nWelcome to Personal Expense Tracker!")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Monthly Summary")
        print("4. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            monthly_summary()
        elif choice == "4":
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
