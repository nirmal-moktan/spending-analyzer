from sqlalchemy import select
from sqlalchemy.orm import Session
from datetime import date

from backend.database import engine
from backend.models import Category, Transaction, ImportHistory

from pathlib import Path
from backend.importer import import_transactions, import_income, calculate_total, reconcile_totals


CATEGORY_MAP_2026 = {
    "Grocery": "Grocery",
    "Clothing and shoes": "Clothing and Shoes",
    "phone bill ": "Phone",
    "Rent+water sewer": "Rent and Water",
    "Eating out": "Eating Out",
    "Internet": "Internet",
    "Health": "Health",
    "Miscellaneous": "Miscellaneous",
    "Gas": "Gas",
    "car + insurance +tax": "Car Expense",
    "Electricity": "Electricity",
    "Laundry": "Laundry",
    "Income": "Salary and Bonus",
}


def get_category_id(session, excel_category, kind):
    category_name = CATEGORY_MAP_2026.get(excel_category)

    if category_name is None:
        raise ValueError(f"Unknown Excel category: {excel_category}")

    category_id = session.scalar(
        select(Category.id).where(
            Category.name == category_name,
            Category.kind == kind
        )
    )

    if category_id is None:
        raise ValueError(f"Category not found in database: {category_name}")

    return category_id


if __name__ == "__main__":
    file_path = Path(__file__).resolve().parent.parent / "data" / "Spend analyser.xlsx"   

    expenses = import_transactions(file_path, "Expense2026",3,33) 
    incomes = import_income(file_path, "Expense2026", 3, 33)

    total_expenses = calculate_total(expenses)
    total_income = calculate_total(incomes)

    reconcile_totals(
        file_path,
        "Expense2026",
        34,
        total_income,
        total_expenses,
        total_income - total_expenses
    )   

    with Session(engine) as session:
        for expense in expenses:
            get_category_id(session, expense["category"], "expense")

        for income in incomes:
            get_category_id(session, income["category"], "income")

        first_expense = expenses[0]

        transaction = Transaction(
            date=first_expense["date"],
            amount=first_expense["amount"],
            type="expense",
            category_id=get_category_id(session, first_expense["category"], "expense"),
            entry_kind="daily_total",
            original_category=first_expense["category"],
            source_cell=first_expense["source_cell"]
        )

        print("Prepared transaction:", transaction.type, transaction.category_id)

        import_record = ImportHistory(
            source_filename=file_path.name,
            worksheet_name="Expense2026",
            period_start=date(2026, 1, 1)
        )

        print("Prepared import:", import_record.worksheet_name)

    print(f"Validated {len(expenses)} expenses and {len(incomes)} income records.")