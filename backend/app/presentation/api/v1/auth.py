"""Presentation: Auth API Routes."""
from fastapi import APIRouter, Depends
from app.presentation.dependencies.container import get_login_uc, get_register_uc
from app.presentation.schemas.auth_schemas import LoginRequest, RegisterRequest, TokenResponse
from app.application.dto.auth_dto import LoginDTO, RegisterDTO

router = APIRouter()

@router.post("/login", response_model=TokenResponse)
async def login(body: LoginRequest, use_case=Depends(get_login_uc)):
    dto = LoginDTO(email=body.email, password=body.password)
    return await use_case.execute(dto)

@router.post("/register", response_model=TokenResponse, status_code=201)
async def register(body: RegisterRequest, use_case=Depends(get_register_uc)):
    dto = RegisterDTO(email=body.email, password=body.password, full_name=body.full_name)
    return await use_case.execute(dto)
