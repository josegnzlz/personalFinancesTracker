import pandas as pd
import csv
from datetime import datetime
from data_entry import get_date, get_amount, get_category, get_description, date_format
import matplotlib.pyplot as plt

class CSV:
    CSV_FILE="finance_data.csv"
    COLUMNS = ["date", "amount", "category", "description"]

    # Solo la propia clase tiene acceso a esta función, no las instancias de la misma
    @classmethod
    def initialice_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=cls.COLUMNS)
            df.to_csv(cls.CSV_FILE, index=False)

    @classmethod
    def add_entry(cls, date, amount, category, description):
        new_entry = {
            "date": datetime.strptime(date, "%Y-%m-%d").strftime("%d-%m-%Y"),
            "amount": amount,
            "category": category,
            "description": description
        }
        # Cuando acabe de usar el fichero, lo cierra automaticamente
        with open(cls.CSV_FILE, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)
            writer.writerow(new_entry)
        print("Entry added successfully")

    @classmethod
    def get_transactions(cls, start_date, end_date):
        df = pd.read_csv(cls.CSV_FILE)
        # Convertimos la columna de fechas en un objeto de fecha
        df["date"] = pd.to_datetime(df["date"], format=date_format)
        start_date = datetime.strptime(start_date, date_format)
        end_date = datetime.strptime(end_date, date_format)
        # MASK: se aplica a las diferentes filas de un dataframe para saber si tenemos o no que seleccionarla
        mask = (df["date"] >= start_date) & (df["date"] <= end_date)
        filtered_df = df.loc[mask] # Solo contiene las filas donde se cumple la condicion de la mascara

        if filtered_df.empty:
            print("No transactions found in the given data range")
        else:
            print(f"Transactions from {start_date.strftime(date_format)} to {end_date.strftime(date_format)}")
            print(
                filtered_df.to_string(
                    index=False, formatters={"date": lambda x: x.strftime(date_format)}
                )
            )

            total_income = filtered_df[filtered_df["category"] == "Income"]["amount"].sum()
            total_expense = filtered_df[filtered_df["category"] == "Expense"]["amount"].sum()
            print("\nSummary:")
            print(f"Total Income: ${total_income:.2f}")
            print(f"Total Expense: ${total_expense:.2f}")
            print(f"Net Savings: ${(total_income - total_expense):.2f}")

        return df

def plot_transactions(df):
    df.set_index("date", inplace=True)
    income_df = (
        df[df["category"] == "Income"]
        .resample("D")
        .sum()
        .reindex(df.index, fill_value=0)
    ) # Para tener una fila para cada dia

    expense_df = (
        df[df["category"] == "Expense"]
        .resample("D")
        .sum()
        .reindex(df.index, fill_value=0)
    )

    plt.figure(figsize=(10,5))
    plt.plot(income_df.index, income_df["amount"], label="Income", color="g")
    plt.plot(expense_df.index, expense_df["amount"], label="Expense", color="r")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Income and Expenses Over Time")
    plt.legend()
    plt.grid(True) # Líneas del gráfico
    plt.show()


def main():
    while True:
        print("\n1. Add a new transaction")
        print("2. View transactions and summary within a date range")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ")

        if choice == "1":
            add()
        elif choice == "2":
            start_date = get_date("Enter the start date (dd-mm-yyyy): ")
            end_date = get_date("Enter the end date (dd-mm-yyyy): ")
            df = CSV.get_transactions(start_date, end_date)
            print(df)
            if input("Do you want to see a plot? (y/n) ").lower() =="y":
                plot_transactions(df)
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Enter 1, 2 or 3.")

# Al ponerlo asi solo se ejecuta al ejecutar main.py, y no si importamos el archivo
if __name__ == "__main__":
    main()