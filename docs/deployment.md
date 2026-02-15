# Deployment Guide

## Development
```bash
docker-compose up --build
```

## Production
1. Set environment variables in `.env`
2. Build Docker images
3. Deploy to cloud provider (AWS/Azure/GCP)
4. Run database migrations: `alembic upgrade head`
