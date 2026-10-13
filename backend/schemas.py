from datetime import date
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, Field


class TransactionCreate(BaseModel):
    # Date of the transaction
    date: date

    # Positive monetary amount, maximum 2 decimal places
    amount: Decimal = Field(gt=0, max_digits=12, decimal_places=2)

    # Only income or expense is allowed
    type: Literal["income", "expense"]

    # Must reference an existing category
    category_id: int = Field(gt=0)

    # Optional description
    description: str | None = Field(default=None, max_length=255)
