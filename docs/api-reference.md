# API Reference

## Base URL
http://localhost:8000/api/v1

## Authentication
All endpoints (except /auth/*) require a Bearer token.

## Endpoints

### Auth
- POST /auth/login
- POST /auth/register

### Suppliers
- GET /suppliers
- GET /suppliers/{id}
- POST /suppliers
- PATCH /suppliers/{id}

### Risk Scores
- POST /risk-scores/{supplier_id}
- GET /risk-scores/{supplier_id}/history

### Alerts
- GET /alerts
- POST /alerts

### Anomalies
- GET /anomalies/supplier/{supplier_id}
- GET /anomalies/unreviewed
- POST /anomalies/detect/{supplier_id}

### Dashboard
- GET /dashboard/summary

### Data Ingestion
- POST /data/upload
