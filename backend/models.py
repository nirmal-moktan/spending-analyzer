from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime, date as PythonDate
from sqlalchemy import DateTime, func, Date, UniqueConstraint, Numeric, CheckConstraint, ForeignKey, String
from decimal import Decimal


class Base(DeclarativeBase):
    pass

class Category(Base):
    __tablename__ = "categories"
    __table_args__ = (
        CheckConstraint(
            "kind IN ('income', 'expense')",
            name="ck_categories_kind"
        ),
        UniqueConstraint(
            "name", "kind", name="uq_categories_name_kind"
        )
    )
    id: Mapped[int] = mapped_column(primary_key = True)
    name: Mapped[str] = mapped_column(String(100), nullable = False)
    kind: Mapped[str] = mapped_column(String(10), nullable=False)

class ImportHistory(Base):
    __tablename__ = "import_history"
    __table_args__ = (
        UniqueConstraint(
            "source_filename",
            "worksheet_name",
            "period_start",
            name="uq_import_source_period"
        ),
    )
    id: Mapped[int] = mapped_column(primary_key=True)
    source_filename: Mapped[str] = mapped_column(String(255), nullable=False)
    worksheet_name: Mapped[str] = mapped_column(String(100), nullable=False)
    imported_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
        )
    period_start: Mapped[PythonDate] = mapped_column(Date, nullable=False)

class Transaction(Base):
    __tablename__ = "transactions"
    __table_args__=(
        CheckConstraint(
            "type IN ('income', 'expense')",
            name="ck_transactions_type"
        ),
        CheckConstraint(
            "entry_kind IN ('daily_total', 'individual')",
            name="ck_transactions_entry_kind"
        ),
        UniqueConstraint(
            "import_id", "source_cell", name="uq_transaction_import_cell"
        ),
        CheckConstraint(
            "amount >= 0",
            name="ck_transactions_amount_nonnegative"
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[PythonDate] = mapped_column(Date, nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(12,2), nullable=False)
    type: Mapped[str] = mapped_column(String(10),nullable=False)
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id"),
        nullable=False
    )
    import_id: Mapped[int | None] = mapped_column(
        ForeignKey("import_history.id"),
        nullable=True
    )
    entry_kind: Mapped[str] = mapped_column(String(20), nullable=False)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    original_category: Mapped[str | None] = mapped_column(String(225), nullable=True)
    source_cell: Mapped[str | None] = mapped_column(String(20), nullable=True)   
