"""Presentation: Data Ingestion API Routes."""
import os
import tempfile
from typing import List
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from app.presentation.dependencies.container import get_supplier_repo
from app.presentation.dependencies.auth import get_current_user
from app.infrastructure.services.csv_parser_service import CSVParserService
from app.domain.entities.supplier import Supplier

router = APIRouter()


@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    supplier_repo=Depends(get_supplier_repo),
    _=Depends(get_current_user),
):
    # Validate file extension
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")

    ext = file.filename.rsplit(".", 1)[-1].lower()
    if ext not in ("csv", "xls", "xlsx"):
        raise HTTPException(status_code=400, detail=f"Unsupported file type: .{ext}. Use CSV or Excel.")

    # Save to temp file
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{ext}") as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")

    # Parse
    try:
        parser = CSVParserService()
        records = await parser.parse(tmp_path)
    except Exception as e:
        os.unlink(tmp_path)
        raise HTTPException(status_code=400, detail=f"Failed to parse file: {str(e)}")
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)

    # Create suppliers from records
    created = 0
    errors = []
    for i, row in enumerate(records):
        try:
            name = str(row.get("name", row.get("supplier_name", ""))).strip()
            country = str(row.get("country", row.get("location", ""))).strip()
            category = str(row.get("category", row.get("type", "General"))).strip()
            email = str(row.get("contact_email", row.get("email", ""))).strip()
            website = str(row.get("website", row.get("url", ""))).strip()

            if not name or not country:
                errors.append(f"Row {i+1}: missing name or country")
                continue

            supplier = Supplier(
                name=name,
                country=country,
                category=category,
                contact_email=email,
                website=website,
            )
            await supplier_repo.create(supplier)
            created += 1
        except Exception as e:
            errors.append(f"Row {i+1}: {str(e)}")

    return {
        "filename": file.filename,
        "total_rows": len(records),
        "created": created,
        "errors": errors[:10],  # Return max 10 errors
    }
