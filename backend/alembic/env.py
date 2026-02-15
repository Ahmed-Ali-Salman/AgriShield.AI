"""Alembic environment configuration for async migrations."""
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context
from app.infrastructure.database.connection import Base
from app.config import settings

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

# Import all models so Alembic can detect them
from app.infrastructure.database.models import *  # noqa
