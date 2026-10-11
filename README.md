# Spending Analyzer

A personal finance application being developed to replace manual Excel expense tracking while preserving historical financial records dating back to 2021.

The goal is to provide a simple interface for recording income and expenses, analyzing spending patterns, and viewing financial history across multiple years.

## Current Development: V0.1 — Excel Importer

The initial version focuses on importing and validating January 2026 financial data from an existing Excel workbook.

### Implemented Features

- Read Excel worksheets using Python and openpyxl.
- Extract daily expenses across 12 categories.
- Extract income records from the Salary/Bonus column.
- Convert financial amounts to `Decimal` for two-decimal-place calculations.
- Validate transaction dates, categories, and amounts.
- Detect Excel formulas with missing cached results.
- Calculate total income, total expenses, and actual savings.
- Reconcile calculated totals against Excel monthly summaries.
- Test core functionality using pytest and synthetic Excel workbooks.

### Technologies Used

**Current:** Python, openpyxl, pytest

**Planned:** FastAPI, PostgreSQL, SQLAlchemy, React, TypeScript, GitHub Actions

## Project Structure

```text
Spend Analyser/
├── backend/
│   ├── importer.py
│   ├── requirements.txt
│   └── tests/
│       └── test_importer.py
├── data/                 # Private, excluded from Git
├── .venv/                # Local Python environment
├── .gitignore
└── README.md
```

## Running Locally

Requires Python and the packages listed in `backend/requirements.txt`.

Install dependencies:

```powershell
python -m pip install -r backend/requirements.txt
```

Run the importer:

```powershell
python backend/importer.py
```

The importer currently expects a local workbook named `Spend analyser.xlsx` inside the `data/` directory, containing an `Expense2026` worksheet.

Run automated tests:

```powershell
python -m pytest -v
```

The tests create synthetic workbooks and do not require the private financial workbook.

## Development Roadmap

**V0.1 — Excel Importer:** Import January 2026 data, validate transactions, calculate financial totals, and reconcile against Excel.

**V1.0 — Full-Stack MVP:** Introduce PostgreSQL persistence, FastAPI endpoints, and a basic React/TypeScript interface for viewing and entering transactions.

**V1.1 — Everyday Usability:** Improve transaction entry, filtering, duplicate prevention, and support for additional 2026 records.

**V2.0 — Financial Analytics:** Add monthly and yearly spending analysis, category comparisons, and visualizations.

**V3.0 — Historical Migration:** Import historical Excel records from 2021–2025 into the same financial database while preserving existing financial history.

## Data Privacy

Real financial records are stored locally and excluded from Git version control.

Automated tests use synthetic transaction data. No personal financial workbooks or sensitive transaction records are intended to be published in the repository.

## Status

Under active development. Currently a command-line Python importer; the database, REST API, and web interface have not yet been implemented.