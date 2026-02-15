"""Presentation: Data Ingestion API Routes."""
from fastapi import APIRouter, Depends, UploadFile, File
from app.presentation.dependencies.container import get_upload_csv_uc
from app.presentation.dependencies.auth import get_current_user

router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...), use_case=Depends(get_upload_csv_uc), _=Depends(get_current_user)):
    # TODO: Save file to temp path, then parse
    return {"message": "File upload endpoint", "filename": file.filename}
