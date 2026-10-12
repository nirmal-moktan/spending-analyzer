from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.database import engine
from backend.models import Category


categories = [
    ("Rent and Water", "expense"),
    ("Grocery", "expense"),
    ("Eating Out", "expense"),
    ("Clothing and Shoes", "expense"),
    ("Laundry", "expense"),
    ("Phone", "expense"),
    ("Internet", "expense"),
    ("Electricity", "expense"),
    ("Health", "expense"),
    ("Gas", "expense"),
    ("Car Expense", "expense"),
    ("Subscriptions", "expense"),
    ("Miscellaneous", "expense"),
    ("Salary and Bonus", "income"),
    ("Passive Income", "income")
]


with Session(engine) as session:
    for name, kind in categories:
        existing = session.scalar(
            select(Category).where(
                Category.name == name,
                Category.kind == kind
            )
        )

        if existing is None:
            session.add(Category(name=name, kind=kind))

    session.commit()

print("Categories initialized successfully.")