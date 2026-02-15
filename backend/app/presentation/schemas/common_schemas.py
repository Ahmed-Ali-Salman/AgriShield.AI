"""Pydantic Schemas: Common (pagination, errors)."""
from typing import Optional, List, Any
from pydantic import BaseModel

class PaginatedResponse(BaseModel):
    items: List[Any]
    total: int
    skip: int
    limit: int

class ErrorResponse(BaseModel):
    detail: str
    code: Optional[str] = None
