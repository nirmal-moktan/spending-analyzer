from sqlalchemy import select, func
from sqlalchemy.orm import Session
from datetime import date

from backend.database import engine
from backend.models import Category, Transaction, ImportHistory

from pathlib import Path
from backend.importer import import_transactions, import_income, calculate_total, reconcile_totals

import sys


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

        existing_import = session.scalar(
            select(ImportHistory.id).where(
                ImportHistory.source_filename == file_path.name,
                ImportHistory.worksheet_name == "Expense2026",
                ImportHistory.period_start == date(2026, 1, 1)
            )
        )

        if existing_import is not None:
            print("January 2026 already imported. skipping.")
            sys.exit(0)

        import_record = ImportHistory(
            source_filename=file_path.name,
            worksheet_name="Expense2026",
            period_start=date(2026, 1, 1)
        )

        print("Prepared import:", import_record.worksheet_name)
        session.add(import_record)
        session.flush()
        print("Generated import ID:", import_record.id)       

        for expense in expenses:
            transaction = Transaction(
                date=expense["date"],
                amount=expense["amount"],
                type="expense",
                category_id=get_category_id(session, expense["category"], "expense"),
                import_id=import_record.id,
                entry_kind="daily_total",
                original_category=expense["category"],
                source_cell=expense["source_cell"]
            )
            session.add(transaction)

        session.flush()
        print("Prepared expenses:", len(expenses))

        for income in incomes:
            transaction = Transaction(
                date=income["date"],
                amount=income["amount"],
                type="income",
                category_id=get_category_id(session, income["category"], "income"),
                import_id=import_record.id,
                entry_kind="daily_total",
                original_category=income["original_category"],
                source_cell=income["source_cell"]
            )

            session.add(transaction)

        session.flush()
        print("Prepared incomes:", len(incomes))

        db_expenses = session.scalar(
            select(func.sum(Transaction.amount)).where(
                Transaction.import_id == import_record.id,
                Transaction.type == "expense"
            )
        )

        db_income = session.scalar(
            select(func.sum(Transaction.amount)).where(
                Transaction.import_id == import_record.id,
                Transaction.type == "income"
            )
        )

        if db_expenses != total_expenses or db_income != total_income:
            raise ValueError("PostgreSQL totals do not match Excel")

        print("Database reconciliation: PASSED")

        session.commit()


    print(f"Validated {len(expenses)} expenses and {len(incomes)} income records.")