# Spending Analyzer

A full-stack personal finance application under development to replace manual Excel expense tracking with a user-friendly web application for recording income, expenses, and savings.

The project also aims to preserve financial records dating back to August 2021 and provide interactive insights into spending patterns, recurring bills, and financial trends.

## Development Status

**V0.1 — Excel Importer: Complete**

**V1.0 — Full-Stack MVP: In Progress**

The Excel importer, PostgreSQL database schema, database migrations, and initial category setup are implemented. Work is underway to connect the importer to PostgreSQL.

The web application and REST API are not yet implemented.

## Implemented Features

### Excel Importer
- Extract January 2026 expenses and income using Python and openpyxl.
- Validate transaction dates, categories, and amounts.
- Use `Decimal` for precise financial calculations.
- Detect Excel formulas with missing cached values.
- Calculate income, expenses, and savings.
- Reconcile calculated totals against Excel monthly summaries.
- Preserve original Excel cell references for traceability.
- Test core importer functionality using pytest and synthetic workbooks.

### PostgreSQL Database
- Connect Python to PostgreSQL using SQLAlchemy and psycopg.
- Define relational models for `categories`, `transactions`, and `import_history`.
- Enforce primary keys, foreign keys, and database constraints.
- Manage database schema changes using Alembic migrations.
- Initialize income and expense categories using a repeatable Python seed script.
- Map historical Excel category names to standardized database categories.
- Validate January 2026 records against database categories.

**Current limitation:** Excel records have not yet been persisted to PostgreSQL. The database import workflow is still being developed.

## Technology Stack

| Component | Technology |
|---|---|
| Backend | Python |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Database driver | psycopg |
| Schema migrations | Alembic |
| Excel processing | openpyxl |
| Testing | pytest |
| Planned API | FastAPI |
| Planned frontend | React + TypeScript |
| Planned CI | GitHub Actions |

## Project Structure

```text
Spend Analyser/
├── backend/
│   ├── database.py
│   ├── models.py
│   ├── importer.py
│   ├── db_import.py
│   ├── seed_categories.py
│   ├── requirements.txt
│   └── tests/
│       └── test_importer.py
├── migrations/
│   ├── versions/
│   └── env.py
├── scripts/
│   └── create_database.sql
├── data/                  # Private Excel data (Git-ignored)
├── alembic.ini
├── .env                   # Local credentials (Git-ignored)
├── .gitignore
└── README.md
```

## Local Setup

**Prerequisites:** Python, PostgreSQL, and Git.

### 1. Install Python dependencies

Create and activate a virtual environment. For Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Install the dependencies:

```powershell
python -m pip install -r backend/requirements.txt
```

### 2. Create the PostgreSQL database

Create a PostgreSQL database named `spending_analyzer`.

The repository includes `scripts/create_database.sql`, which can be executed through pgAdmin's Query Tool while connected to an existing administrative database such as `postgres`.

### 3. Configure environment variables

Create a `.env` file in the project root:

```dotenv
DB_HOST=localhost
DB_PORT=5432
DB_NAME=spending_analyzer
DB_USER=postgres
DB_PASSWORD=YOUR_PASSWORD
```

Replace `YOUR_PASSWORD` with your local PostgreSQL password. Use appropriate credentials for your own environment.

Never commit `.env` to Git.

### 4. Apply database migrations

```powershell
python -m alembic upgrade head
```

This creates the application tables in PostgreSQL.

### 5. Initialize categories

```powershell
python -m backend.seed_categories
```

This adds the initial income and expense categories while skipping existing entries, making the script safe to rerun.

### 6. Verify the database connection

```powershell
python -m backend.database
```

Expected output:

```text
Connected to: spending_analyzer
```

## Running the Excel Importer

The importer currently expects a private workbook named `Spend analyser.xlsx` inside the `data/` directory.

The workbook is not included in this repository.

Run the original Excel validation and reconciliation:

```powershell
python backend/importer.py
```

Run the current database import preparation workflow:

```powershell
python -m backend.db_import
```

The database import preparation currently validates category mappings, checks financial totals, and prepares example SQLAlchemy objects. It does **not** yet save the imported financial transactions to PostgreSQL.

## Testing

Run the automated tests:

```powershell
python -m pytest backend/tests -v
```

Tests use synthetic Excel workbooks rather than private financial data.

Additional database and API tests are planned as development progresses.

## Development Roadmap

**V0.1 — Excel Importer (Complete)**

Parse January 2026 financial records, validate data, calculate totals, and reconcile against Excel.

**V1.0 — Full-Stack MVP (In Progress)**

Implement PostgreSQL persistence, reliable import handling, FastAPI endpoints, manual income/expense entry, and a basic React/TypeScript dashboard.

**V1.1 — Everyday Usability**

Expand 2026 imports, support transaction editing, filtering, and searching, and improve the daily expense-tracking experience.

**V2.0 — Financial Analytics**

Introduce interactive charts, category comparisons, recurring-bill trends, richer transaction details, and improved user experience.

**V3.0 — Historical Integration**

Migrate historical records from 2021–2025 into the same database while preserving original amounts and category information.

**V4.0 — Optional Predictive Analytics**

Explore statistical or machine-learning approaches to forecasting expenses and identifying seasonal spending patterns.

## Design Principles

- Prioritize accurate financial records and calculations.
- Preserve historical Excel data without inventing missing information.
- Make future transaction entry easier than Excel.
- Keep category management flexible without unnecessary complexity.
- Prevent duplicate imports and accidental modification of historical data.
- Preserve original purchases and track future refunds without deleting transaction history.
- Separate ordinary income and expenses from future transfers and investment-related activities.
- Develop functionality incrementally with testing and maintainable code.

## Data Privacy

Real financial records, database credentials, and local Excel workbooks are excluded from Git version control.

Automated tests use synthetic financial data. Public demonstrations should use synthetic records rather than personal financial information.

## Project Goal

Build a reliable, maintainable full-stack application that eventually replaces Excel for everyday household financial tracking while supporting increasingly sophisticated financial analysis.

The project also serves as hands-on software engineering experience in backend development, relational database design, testing, API development, and full-stack application architecture.