---
sidebar_position: 3
title: Công nghệ sử dụng
---

# Công nghệ sử dụng

## Framework và Runtime

### Spring Boot 3.3.1
- **Mục đích**: Framework chính để xây dựng RESTful API
- **Tính năng**: 
  - Auto-configuration
  - Embedded server (Tomcat)
  - Production-ready features
  - Dependency injection

### Java 17
- **Version**: JDK 17 (LTS)
- **Lý do chọn**: 
  - Hỗ trợ tốt bởi Spring Boot 3.x
  - Performance improvements
  - Modern language features

## Database

### MongoDB
- **Version**: Sử dụng Spring Data MongoDB
- **Mục đích**: NoSQL database để lưu trữ datasets và users
- **Tính năng sử dụng**:
  - Spring Data MongoDB Repository
  - MongoDB Aggregation Framework
  - Indexing (unique index cho username)
  - Auditing (createdAt, updatedAt tự động)

## Security

### Spring Security
- **Mục đích**: Authentication và Authorization
- **Tính năng**:
  - JWT-based authentication
  - Stateless session management
  - CORS configuration
  - Password encoding (BCrypt)

### JWT (JSON Web Token)
- **Library**: `io.jsonwebtoken:jjwt` (version 0.11.5)
- **Mục đích**: Token-based authentication
- **Algorithm**: HS256
- **Storage**: HttpOnly cookie

### BCrypt
- **Mục đích**: Password hashing
- **Tích hợp**: Qua Spring Security PasswordEncoder

## API Documentation

### SpringDoc OpenAPI
- **Version**: 2.5.0
- **Mục đích**: Tự động generate API documentation
- **UI**: Swagger UI
- **Access**: `/swagger-ui/index.html`

## Data Mapping

### MapStruct
- **Version**: 1.5.5.Final
- **Mục đích**: Type-safe mapping giữa Entity và DTO
- **Lợi ích**:
  - Compile-time code generation
  - Type safety
  - Performance tốt hơn reflection-based mappers

## Utilities

### Lombok
- **Version**: 1.18.30
- **Mục đích**: Giảm boilerplate code
- **Annotations sử dụng**:
  - `@Data`: Generate getters, setters, toString, equals, hashCode
  - `@Builder`: Builder pattern
  - `@RequiredArgsConstructor`: Constructor injection
  - `@NoArgsConstructor`, `@AllArgsConstructor`

### Jakarta Validation
- **Mục đích**: Input validation
- **Annotations**: `@NotEmpty`, `@Valid`

## Build Tool

### Maven
- **Mục đích**: Dependency management và build
- **Plugins**:
  - Spring Boot Maven Plugin
  - Maven Compiler Plugin (với annotation processors)

## Dependencies chính

```xml
<!-- Web -->
spring-boot-starter-web

<!-- Database -->
spring-boot-starter-data-mongodb

<!-- Security -->
spring-boot-starter-security

<!-- API Documentation -->
springdoc-openapi-starter-webmvc-ui (2.5.0)

<!-- JWT -->
jjwt-api, jjwt-impl, jjwt-jackson (0.11.5)

<!-- Mapping -->
mapstruct (1.5.5.Final)

<!-- Utilities -->
lombok (1.18.30)
spring-boot-starter-validation
```

## Development Tools

### Spring Boot DevTools (nếu có)
- Hot reload
- Auto restart

## Testing (Dependencies)

- `spring-boot-starter-test`: Unit và integration testing
- `spring-security-test`: Security testing utilities

## Logging

- **Framework**: Logback (mặc định của Spring Boot)
- **Configuration**: Qua `application.properties`
- **Level**: DEBUG cho Spring Security (development)

## CORS Configuration

- **Custom CORS**: Được cấu hình trong `SecurityConfig`
- **Allowed Origins**: 
  - Localhost với mọi port
  - Production domains
- **Credentials**: Enabled (cho cookie support)

## Version Summary

| Technology | Version |
|------------|---------|
| Spring Boot | 3.3.1 |
| Java | 17 |
| MongoDB Driver | (via Spring Data) |
| SpringDoc OpenAPI | 2.5.0 |
| JWT (jjwt) | 0.11.5 |
| MapStruct | 1.5.5.Final |
| Lombok | 1.18.30 |

## Tại sao chọn các công nghệ này?

1. **Spring Boot**: 
   - Industry standard cho Java REST APIs
   - Rich ecosystem
   - Excellent documentation

2. **MongoDB**: 
   - Flexible schema cho datasets
   - Good performance cho read-heavy workloads
   - Easy horizontal scaling

3. **JWT**: 
   - Stateless authentication
   - Scalable
   - Industry standard

4. **MapStruct**: 
   - Type-safe mapping
   - Compile-time generation (fast)
   - No runtime overhead

5. **Lombok**: 
   - Reduces boilerplate
   - Improves code readability
   - Widely adopted

