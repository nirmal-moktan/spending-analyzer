
from datetime import date
from decimal import Decimal

from sqlalchemy import select, func, extract
from sqlalchemy.orm import Session

from backend.database import engine
from backend.models import Transaction, Category


# Retrieve 5 transactions with their category names
def get_transactions(session):
    statement = (
        select(Transaction.date, Category.name, Transaction.amount)
        .join(Category, Transaction.category_id == Category.id)
        .order_by(Transaction.date, Transaction.id)
        .limit(5)
    )

    return session.execute(statement).all()


# Calculate income, expenses, and savings for a given month
def get_monthly_summary(session, year, month):

    # Define the beginning of the selected month
    start_date = date(year, month, 1)

    # Define the beginning of the following month
    if month == 12:
        end_date = date(year + 1, 1, 1)
    else:
        end_date = date(year, month + 1, 1)

    # Sum transaction amounts separately for income and expenses
    statement = (
        select(Transaction.type, func.sum(Transaction.amount))
        .where(
            Transaction.date >= start_date,
            Transaction.date < end_date
        )
        .group_by(Transaction.type)
    )

    # Convert query results into a dictionary
    totals = dict(session.execute(statement).all())

    # Default to zero if the month has no income or expenses
    income = totals.get("income", Decimal("0.00"))
    expenses = totals.get("expense", Decimal("0.00"))

    # Calculate net savings
    savings = income - expenses

    return income, expenses, savings


def get_category_totals(session, year, month):
    # Define the selected month's date range
    start_date = date(year, month, 1)

    if month == 12:
        end_date = date(year + 1, 1, 1)
    else:
        end_date = date(year, month + 1, 1)

    # Calculate total expenses for each category
    statement = (
        select(Category.name, func.sum(Transaction.amount))
        .join(Category, Transaction.category_id == Category.id)
        .where(
            Transaction.type == "expense",
            Transaction.date >= start_date,
            Transaction.date < end_date
        )
        .group_by(Category.name)
        .order_by(Category.name)
    )

    return session.execute(statement).all()


def get_yearly_category_totals(session, year):
    # Extract the month number from each transaction date
    month_number = extract("month", Transaction.date)

    statement = (
        select(
            Category.name,
            month_number,
            func.sum(Transaction.amount)
        )
        .join(Category, Transaction.category_id == Category.id)
        .where(
            Transaction.type == "expense",
            Transaction.date >= date(year, 1, 1),
            Transaction.date < date(year + 1, 1, 1)
        )
        .group_by(Category.name, month_number)
        .order_by(Category.name, month_number)
    )

    return session.execute(statement).all()


def main():
    # Open a database session
    with Session(engine) as session:

        # Display the first 5 transactions
        print("First 5 transactions:")

        for transaction_date, category, amount in get_transactions(session):
            print(transaction_date, category, amount)

        # Calculate January 2026 financial summary
        income, expenses, savings = get_monthly_summary(
            session, 2026, 1
        )

        print("\nJanuary 2026 Summary:")
        print(f"Income: ${income:.2f}")
        print(f"Expenses: ${expenses:.2f}")
        print(f"Savings: ${savings:.2f}")


if __name__ == "__main__":
    main()
