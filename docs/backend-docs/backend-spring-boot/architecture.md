---
sidebar_position: 2
title: Thiết kế hệ thống
---

# Thiết kế hệ thống

## Kiến trúc tổng thể

Hệ thống được thiết kế theo mô hình **Layered Architecture** (Kiến trúc phân lớp) với các tầng rõ ràng:

```
┌─────────────────────────────────────────────────────────┐
│                    Presentation Layer                    │
│              (Controllers - REST Endpoints)             │
├─────────────────────────────────────────────────────────┤
│                     Business Layer                       │
│              (Services - Business Logic)                │
├─────────────────────────────────────────────────────────┤
│                      Data Access Layer                   │
│            (Repositories - Database Access)             │
├─────────────────────────────────────────────────────────┤
│                      Data Layer                          │
│                   (MongoDB Database)                    │
└─────────────────────────────────────────────────────────┘
```

## Cấu trúc Package

```
io.ldxinsight
├── config/              # Configuration classes
│   ├── ApplicationConfig.java
│   ├── SecurityConfig.java
│   ├── JwtAuthFilter.java
│   └── OpenApiConfig.java
├── controller/          # REST Controllers
│   ├── AuthController.java
│   ├── DatasetController.java
│   └── StatisticsController.java
├── service/            # Business Logic
│   ├── AuthService.java
│   ├── DatasetService.java
│   ├── JwtService.java
│   ├── JwtCookieService.java
│   └── impl/
│       ├── AuthServiceImpl.java
│       └── DatasetServiceImpl.java
├── repository/         # Data Access
│   ├── UserRepository.java
│   └── DatasetRepository.java
├── model/              # Domain Models
│   ├── User.java
│   ├── Dataset.java
│   └── Role.java
├── dto/                # Data Transfer Objects
│   ├── AuthResponse.java
│   ├── LoginRequest.java
│   ├── RegisterRequest.java
│   ├── DatasetDto.java
│   ├── CreateDatasetRequest.java
│   └── StatSummaryDto.java
├── mapper/             # Entity-DTO Mappers
│   ├── AuthMapper.java
│   └── DatasetMapper.java
└── exception/          # Exception Handling
    ├── GlobalExceptionHandler.java
    ├── ResourceNotFoundException.java
    └── DuplicateResourceException.java
```

## Các Layer chi tiết

### 1. Presentation Layer (Controller)

**Trách nhiệm**:
- Nhận HTTP requests
- Validate input
- Gọi service layer
- Trả về HTTP responses
- Xử lý HTTP status codes

**Controllers**:
- `AuthController`: Authentication endpoints
- `DatasetController`: Dataset CRUD và search
- `StatisticsController`: Statistics endpoints

**Pattern**: RESTful API design

### 2. Business Layer (Service)

**Trách nhiệm**:
- Business logic
- Data transformation
- Transaction management
- Exception handling

**Services**:
- `AuthService`: Authentication logic
- `DatasetService`: Dataset business logic
- `JwtService`: JWT token generation/validation
- `JwtCookieService`: Cookie management

**Pattern**: Interface-based design (Service interface + Implementation)

### 3. Data Access Layer (Repository)

**Trách nhiệm**:
- Database operations
- Query execution
- Data persistence

**Repositories**:
- `UserRepository`: User data access
- `DatasetRepository`: Dataset data access

**Pattern**: Spring Data MongoDB Repository

### 4. Data Layer (MongoDB)

**Collections**:
- `users`: User accounts
- `datasets`: Dataset information

## Design Patterns

### 1. Repository Pattern
- Tách biệt data access logic
- Dễ dàng test và maintain
- Sử dụng Spring Data MongoDB

### 2. Service Pattern
- Tách biệt business logic
- Interface-based design
- Dependency injection

### 3. DTO Pattern
- Tách biệt internal models và external API
- Bảo vệ domain models
- Versioning API dễ dàng hơn

### 4. Mapper Pattern
- MapStruct để convert Entity ↔ DTO
- Type-safe
- Compile-time generation

### 5. Exception Handling Pattern
- Global exception handler
- Custom exceptions
- Consistent error responses

## Security Architecture

### Authentication Flow

```
1. Client → POST /api/v1/auth/login
2. AuthController → AuthService.login()
3. AuthenticationManager.authenticate()
4. JwtService.generateToken()
5. JwtCookieService.createJwtCookie()
6. Response với HttpOnly cookie
```

### Authorization Flow

```
1. Client request với cookie
2. JwtAuthFilter extracts token từ cookie
3. JwtService validates token
4. UserDetailsService loads user
5. SecurityContext set authentication
6. Controller method executes
```

### Security Components

- **SecurityConfig**: Cấu hình security rules
- **JwtAuthFilter**: Filter để validate JWT
- **JwtService**: JWT operations
- **ApplicationConfig**: UserDetailsService, PasswordEncoder

## Data Flow

### Read Operation (GET)

```
Client Request
    ↓
Controller
    ↓
Service
    ↓
Repository
    ↓
MongoDB
    ↓
Mapper (Entity → DTO)
    ↓
Controller Response
```

### Write Operation (POST/PUT/DELETE)

```
Client Request
    ↓
Controller (Validation)
    ↓
Service (Business Logic)
    ↓
Mapper (DTO → Entity)
    ↓
Repository (Save)
    ↓
MongoDB
    ↓
Response
```

## API Design Principles

### RESTful Conventions

- **GET**: Read operations
- **POST**: Create operations
- **PUT**: Update operations
- **DELETE**: Delete operations

### URL Structure

```
/api/v1/{resource}/{id}/{action}
```

Examples:
- `GET /api/v1/datasets` - List datasets
- `GET /api/v1/datasets/{id}` - Get dataset by ID
- `POST /api/v1/datasets` - Create dataset
- `GET /api/v1/datasets/categories` - Get all categories

### Response Format

**Success Response**:
```json
{
  "data": {...}
}
```

**Error Response**:
```json
{
  "timestamp": "2025-01-01T00:00:00",
  "status": 404,
  "error": "Not Found",
  "message": "Resource not found"
}
```

## Database Schema

### User Collection

```javascript
{
  _id: ObjectId,
  username: String (unique, indexed),
  password: String (hashed),
  role: Enum (ROLE_USER, ROLE_ADMIN),
  createdAt: Instant,
  updatedAt: Instant
}
```

### Dataset Collection

```javascript
{
  _id: ObjectId,
  title: String,
  description: String,
  source: String,
  tags: [String],
  category: String,
  dataUrl: String,
  provider: String,
  viewCount: Number,
  downloadCount: Number,
  createdAt: Instant,
  updatedAt: Instant
}
```

## Cross-Cutting Concerns

### 1. Logging
- Spring Boot default logging (Logback)
- Security debug logging

### 2. Exception Handling
- `GlobalExceptionHandler` xử lý tất cả exceptions
- Custom exceptions với HTTP status codes

### 3. Validation
- Jakarta Validation
- Request body validation
- Path variable validation

### 4. CORS
- Configured trong SecurityConfig
- Support multiple origins
- Credentials enabled

## Scalability Considerations

### Current Design
- Stateless authentication (JWT)
- MongoDB horizontal scaling support
- Stateless services

### Future Improvements
- Caching layer (Redis)
- Load balancing
- Database replication
- API rate limiting

## Testing Strategy

### Unit Tests
- Service layer logic
- Utility methods
- Mappers

### Integration Tests
- Repository layer
- Controller endpoints
- Security configuration

### Test Dependencies
- `spring-boot-starter-test`
- `spring-security-test`

## Configuration Management

### application.properties
- Database connection
- Server port
- JWT secret
- Logging configuration

### Environment Variables
- `MONGO_URI`: MongoDB connection string
- `JWT_SECRET`: JWT secret key

## Deployment Architecture

```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │ HTTP/HTTPS
       ↓
┌─────────────┐
│ Spring Boot │
│ Application │
└──────┬──────┘
       │
       ↓
┌─────────────┐
│   MongoDB   │
└─────────────┘
```

## Best Practices Implemented

1. **Separation of Concerns**: Rõ ràng giữa các layers
2. **Dependency Injection**: Spring IoC container
3. **Interface-based Design**: Dễ test và maintain
4. **DTO Pattern**: Bảo vệ domain models
5. **Exception Handling**: Centralized error handling
6. **Security**: JWT + HttpOnly cookies
7. **API Documentation**: Swagger/OpenAPI
8. **Validation**: Input validation
9. **Auditing**: Automatic timestamp tracking
10. **CORS**: Proper CORS configuration

