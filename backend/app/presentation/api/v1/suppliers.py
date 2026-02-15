"""
Presentation: Supplier API Routes.
"""

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.presentation.schemas.supplier_schemas import (
    SupplierCreateRequest,
    SupplierUpdateRequest,
    SupplierResponse,
)
from app.presentation.dependencies.container import (
    get_create_supplier_uc,
    get_get_supplier_uc,
    get_list_suppliers_uc,
    get_update_supplier_uc,
)
from app.presentation.dependencies.auth import get_current_user
from app.application.dto.supplier_dto import CreateSupplierDTO, UpdateSupplierDTO

router = APIRouter()


@router.get("/", response_model=List[SupplierResponse])
async def list_suppliers(
    skip: int = 0,
    limit: int = 20,
    use_case=Depends(get_list_suppliers_uc),
    _user=Depends(get_current_user),
):
    """List all suppliers with pagination."""
    return await use_case.execute(skip=skip, limit=limit)


@router.get("/{supplier_id}", response_model=SupplierResponse)
async def get_supplier(
    supplier_id: UUID,
    use_case=Depends(get_get_supplier_uc),
    _user=Depends(get_current_user),
):
    """Get a single supplier by ID."""
    result = await use_case.execute(supplier_id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Supplier not found")
    return result


@router.post("/", response_model=SupplierResponse, status_code=status.HTTP_201_CREATED)
async def create_supplier(
    body: SupplierCreateRequest,
    use_case=Depends(get_create_supplier_uc),
    _user=Depends(get_current_user),
):
    """Create a new supplier."""
    dto = CreateSupplierDTO(
        name=body.name,
        country=body.country,
        category=body.category,
        contact_email=body.contact_email,
        website=body.website,
    )
    return await use_case.execute(dto)


@router.patch("/{supplier_id}", response_model=SupplierResponse)
async def update_supplier(
    supplier_id: UUID,
    body: SupplierUpdateRequest,
    use_case=Depends(get_update_supplier_uc),
    _user=Depends(get_current_user),
):
    """Update a supplier."""
    dto = UpdateSupplierDTO(
        name=body.name,
        country=body.country,
        category=body.category,
        contact_email=body.contact_email,
        website=body.website,
    )
    return await use_case.execute(supplier_id, dto)
