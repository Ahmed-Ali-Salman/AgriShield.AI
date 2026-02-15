# Architecture

AgriShield AI follows a SOLID, four-layer architecture:

## Layers
1. **Domain** - Pure business logic, entities, value objects, interfaces
2. **Application** - Use cases, DTOs, orchestration
3. **Infrastructure** - Database, ML, external services, security
4. **Presentation** - API routes, schemas, middleware

## SOLID Principles Applied
- **S**: Each file has a single responsibility
- **O**: Domain interfaces allow extension without modification
- **L**: All repository implementations are interchangeable
- **I**: Small, focused interfaces per entity
- **D**: Domain/Application depend on abstractions; Infrastructure provides implementations
