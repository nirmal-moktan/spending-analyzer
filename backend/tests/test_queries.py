from datetime import date
from decimal import Decimal

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from backend.models import Base, Category, Transaction
from backend.queries import get_monthly_summary


@pytest.fixture
def db_session():
    # Create a temporary SQLite database in memory.
    # This does NOT affect our real PostgreSQL database.
    test_engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(test_engine)

    with Session(test_engine) as session:
        # Create synthetic categories for testing.
        grocery = Category(name="Grocery", kind="expense")
        salary = Category(name="Salary and Bonus", kind="income")

        session.add_all([grocery, salary])
        session.flush()

        yield session, grocery.id, salary.id

    test_engine.dispose()


def add_transaction(session, category_id, kind, transaction_date, amount):
    # Helper function to create synthetic transactions.
    transaction = Transaction(
        date=transaction_date,
        amount=Decimal(amount),
        type=kind,
        category_id=category_id,
        entry_kind="individual"
    )

    session.add(transaction)
    session.flush()


def test_empty_month(db_session):
    session, grocery_id, salary_id = db_session

    income, expenses, savings = get_monthly_summary(session, 2026, 1)

    assert income == Decimal("0.00")
    assert expenses == Decimal("0.00")
    assert savings == Decimal("0.00")


def test_income_only(db_session):
    session, grocery_id, salary_id = db_session

    add_transaction(session, salary_id, "income", date(2026, 1, 5), "2000.00")

    income, expenses, savings = get_monthly_summary(session, 2026, 1)

    assert income == Decimal("2000.00")
    assert expenses == Decimal("0.00")
    assert savings == Decimal("2000.00")


def test_negative_savings(db_session):
    session, grocery_id, salary_id = db_session

    add_transaction(session, salary_id, "income", date(2026, 1, 5), "1000.00")
    add_transaction(session, grocery_id, "expense", date(2026, 1, 7), "1200.00")

    income, expenses, savings = get_monthly_summary(session, 2026, 1)

    assert income == Decimal("1000.00")
    assert expenses == Decimal("1200.00")
    assert savings == Decimal("-200.00")


def test_month_boundary(db_session):
    session, grocery_id, salary_id = db_session

    add_transaction(session, grocery_id, "expense", date(2026, 1, 31), "50.00")
    add_transaction(session, grocery_id, "expense", date(2026, 2, 1), "75.00")

    income, expenses, savings = get_monthly_summary(session, 2026, 1)

    # February's expense must not be included in January.
    assert expenses == Decimal("50.00")
    assert savings == Decimal("-50.00")
