from fastapi import FastAPI, Query
from sqlalchemy.orm import Session

from backend.database import engine
from backend.queries import get_monthly_summary, get_category_totals

from decimal import Decimal
from backend.queries import get_yearly_category_totals


app = FastAPI(title="Spending Analyzer API")


@app.get("/api/summary")
def monthly_summary(year: int, month: int = Query(ge=1, le=12)):

    with Session(engine) as session:
        income, expenses, savings = get_monthly_summary(
            session, year, month
        )

    return {
        "year": year,
        "month": month,
        "income": str(income),
        "expenses": str(expenses),
        "savings": str(savings)
    }



@app.get("/api/category-totals")
def category_totals(year: int, month: int = Query(ge=1, le=12)):

    # Open a database session
    with Session(engine) as session:
        results = get_category_totals(session, year, month)

    # Convert database results into JSON-friendly dictionaries
    categories = [
        {"category": name, "total": str(total)}
        for name, total in results
    ]

    return {
        "year": year,
        "month": month,
        "categories": categories
    }



@app.get("/api/yearly-category-totals")
def yearly_category_totals(year: int):

    # Retrieve category totals for each month from PostgreSQL
    with Session(engine) as session:
        results = get_yearly_category_totals(session, year)

    # Start with zero expenses for all 12 months
    monthly_totals = {m: Decimal("0.00") for m in range(1, 13)}
    categories = {}

    # Organize the database results by category and month
    for name, month, amount in results:
        month = int(month)

        if name not in categories:
            categories[name] = {
                m: Decimal("0.00") for m in range(1, 13)
            }

        categories[name][month] = amount
        monthly_totals[month] += amount

    # Prepare JSON with monthly and yearly totals
    return {
        "year": year,
        "categories": [
            {
                "category": name,
                "months": {
                    str(m): str(amount)
                    for m, amount in months.items()
                },
                "year_total": str(sum(months.values()))
            }
            for name, months in categories.items()
        ],
        "monthly_totals": {
            str(m): str(amount)
            for m, amount in monthly_totals.items()
        },
        "grand_total": str(sum(monthly_totals.values()))
    }

