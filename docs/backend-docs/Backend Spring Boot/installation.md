---
sidebar_position: 4
title: Hướng dẫn cài đặt và chạy trên Local
---

# Hướng dẫn cài đặt và chạy trên Local

## Yêu cầu hệ thống

### Phần mềm cần thiết

1. **Java Development Kit (JDK)**
   - Version: **JDK 17** trở lên
   - Download: [Oracle JDK](https://www.oracle.com/java/technologies/downloads/#java17) hoặc [OpenJDK](https://adoptium.net/)
   - Kiểm tra: `java -version`

2. **Maven**
   - Version: **3.6+** (hoặc sử dụng Maven Wrapper có sẵn)
   - Download: [Maven Download](https://maven.apache.org/download.cgi)
   - Kiểm tra: `mvn -version`

3. **MongoDB**
   - Version: **4.4+** (khuyến nghị 5.0+)
   - Download: [MongoDB Community Server](https://www.mongodb.com/try/download/community)
   - Hoặc sử dụng Docker: `docker run -d -p 27017:27017 mongo:latest`

4. **IDE (Tùy chọn)**
   - IntelliJ IDEA (khuyến nghị)
   - Eclipse
   - VS Code với Java extensions

## Các bước cài đặt

### Bước 1: Clone Repository

```bash
git clone <repository-url>
cd Ldx-Insight/backend/ldx-insight-backend
```

### Bước 2: Cài đặt MongoDB

#### Option A: Cài đặt MongoDB Local

1. Download và cài đặt MongoDB từ [mongodb.com](https://www.mongodb.com/try/download/community)

2. Khởi động MongoDB service:
   ```bash
   # Windows
   net start MongoDB
   
   # Linux/Mac
   sudo systemctl start mongod
   # hoặc
   mongod
   ```

3. Kiểm tra MongoDB đang chạy:
   ```bash
   mongosh
   # hoặc
   mongo
   ```

#### Option B: Sử dụng Docker

```bash
docker run -d \
  --name mongodb \
  -p 27017:27017 \
  -v mongodb-data:/data/db \
  mongo:latest
```

### Bước 3: Cấu hình Environment Variables

Tạo file `.env` hoặc set environment variables:

```bash
# Windows (PowerShell)
$env:MONGO_URI="mongodb://localhost:27017/ldx-insight-db"
$env:JWT_SECRET="your-secret-key-here"

# Linux/Mac
export MONGO_URI="mongodb://localhost:27017/ldx-insight-db"
export JWT_SECRET="your-secret-key-here"
```

**Lưu ý**: Nếu không set environment variables, hệ thống sẽ sử dụng giá trị mặc định trong `application.properties`.

### Bước 4: Cấu hình JWT Secret Key

Mở file `src/main/resources/application.properties` và kiểm tra:

```properties
jwt.secret-key=${JWT_SECRET:TGR4SW5zaWdodDIwMjVTZWNyZXRLZXlGb3JKV1RUb2tlbkdlbmVyYXRpb25BbmRWYWxpZGF0aW9uTXVzdEJlU2VjdXJlQW5kTG9uZ0Vub3VnaA==}
```

**Quan trọng**: 
- Secret key mặc định chỉ dùng cho development
- Production nên dùng secret key mạnh hơn và lưu trong environment variable

### Bước 5: Build Project

Sử dụng Maven Wrapper (khuyến nghị):

```bash
# Windows
.\mvnw.cmd clean install

# Linux/Mac
./mvnw clean install
```

Hoặc sử dụng Maven đã cài đặt:

```bash
mvn clean install
```

### Bước 6: Chạy Application

#### Option A: Sử dụng Maven

```bash
# Windows
.\mvnw.cmd spring-boot:run

# Linux/Mac
./mvnw spring-boot:run
```

#### Option B: Chạy từ IDE

1. Mở project trong IDE (IntelliJ IDEA, Eclipse, etc.)
2. Tìm class `LdxInsightBackendApplication.java`
3. Right-click → Run `LdxInsightBackendApplication`

#### Option C: Chạy JAR file

```bash
# Build JAR
mvn clean package

# Chạy JAR
java -jar target/ldx-insight-backend-0.0.1-SNAPSHOT.jar
```

### Bước 7: Kiểm tra Application

1. **Kiểm tra server đang chạy**:
   - Mở browser: `http://localhost:8080`
   - Hoặc kiểm tra logs trong console

2. **Truy cập Swagger UI**:
   - URL: `http://localhost:8080/swagger-ui/index.html`
   - Xem tất cả API endpoints và test trực tiếp

3. **Test API**:
   ```bash
   # Health check (nếu có)
   curl http://localhost:8080/api/v1/datasets
   
   # Hoặc sử dụng Postman/Insomnia
   ```

## Cấu hình chi tiết

### application.properties

File cấu hình chính: `src/main/resources/application.properties`

```properties
# Server
server.port=8080

# MongoDB
spring.data.mongodb.database=ldx-insight-db
spring.data.mongodb.uri=mongodb://localhost:27017/ldx-insight-db

# Swagger
springdoc.swagger-ui.path=/swagger-ui.html
springdoc.api-docs.path=/v3/api-docs

# JWT
jwt.secret-key=${JWT_SECRET:default-secret-key}
jwt.cookie-name=ldx_access_token

# Logging
logging.level.org.springframework.security=DEBUG
logging.file.name=logs/spring-security-debug.log
```

### Thay đổi Port

Nếu port 8080 đã được sử dụng, thay đổi trong `application.properties`:

```properties
server.port=8081
```

### Thay đổi MongoDB Connection

```properties
# Local MongoDB
spring.data.mongodb.uri=mongodb://localhost:27017/ldx-insight-db

# MongoDB Atlas (Cloud)
spring.data.mongodb.uri=mongodb+srv://username:password@cluster.mongodb.net/ldx-insight-db

# MongoDB với authentication
spring.data.mongodb.uri=mongodb://username:password@localhost:27017/ldx-insight-db
```

## Troubleshooting

### Lỗi: Port đã được sử dụng

```
Error: Port 8080 is already in use
```

**Giải pháp**:
1. Tìm process đang dùng port 8080:
   ```bash
   # Windows
   netstat -ano | findstr :8080
   
   # Linux/Mac
   lsof -i :8080
   ```
2. Kill process hoặc đổi port trong `application.properties`

### Lỗi: MongoDB connection failed

```
Cannot connect to MongoDB
```

**Giải pháp**:
1. Kiểm tra MongoDB đang chạy:
   ```bash
   # Windows
   net start MongoDB
   
   # Linux/Mac
   sudo systemctl status mongod
   ```
2. Kiểm tra connection string trong `application.properties`
3. Kiểm tra firewall settings

### Lỗi: JWT secret key invalid

```
Invalid JWT secret key
```

**Giải pháp**:
1. Đảm bảo secret key là Base64 encoded hoặc plain text hợp lệ
2. Secret key phải có độ dài tối thiểu 32 bytes (256 bits) cho HS256
3. Set environment variable `JWT_SECRET` với giá trị hợp lệ

### Lỗi: Build failed

```
Maven build failed
```

**Giải pháp**:
1. Kiểm tra Java version: `java -version` (phải là 17+)
2. Xóa cache Maven: `mvn clean`
3. Update Maven dependencies: `mvn dependency:resolve`
4. Kiểm tra internet connection (để download dependencies)

### Lỗi: Lombok không hoạt động

**Giải pháp**:
1. Enable annotation processing trong IDE
2. IntelliJ IDEA: Settings → Build → Compiler → Annotation Processors → Enable
3. Rebuild project

## Development Tips

### Hot Reload

Sử dụng Spring Boot DevTools (nếu được thêm vào dependencies):

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-devtools</artifactId>
    <scope>runtime</scope>
    <optional>true</optional>
</dependency>
```

### Debug Mode

Chạy với debug mode:

```bash
mvn spring-boot:run -Dspring-boot.run.jvmArguments="-Xdebug -Xrunjdwp:transport=dt_socket,server=y,suspend=n,address=5005"
```

### Logging

Xem logs trong console hoặc file `logs/spring-security-debug.log`

### Database Management

Sử dụng MongoDB Compass hoặc mongosh để quản lý database:

```bash
mongosh
use ldx-insight-db
show collections
db.datasets.find()
```

## Kiểm tra sau khi cài đặt

### Checklist

- [ ] Java 17+ đã cài đặt
- [ ] Maven đã cài đặt hoặc sử dụng Maven Wrapper
- [ ] MongoDB đang chạy
- [ ] Application build thành công
- [ ] Application chạy không lỗi
- [ ] Swagger UI truy cập được: `http://localhost:8080/swagger-ui/index.html`
- [ ] API endpoints hoạt động

### Test API Endpoints

1. **Get all datasets**:
   ```bash
   curl http://localhost:8080/api/v1/datasets
   ```

2. **Register user**:
   ```bash
   curl -X POST http://localhost:8080/api/v1/auth/register \
     -H "Content-Type: application/json" \
     -d '{"username":"testuser","password":"testpass123"}'
   ```

3. **Get categories**:
   ```bash
   curl http://localhost:8080/api/v1/datasets/categories
   ```

## Next Steps

Sau khi cài đặt thành công:

1. Đọc tài liệu API tại Swagger UI
2. Xem [Architecture Documentation](./architecture.md)
3. Xem [Technologies Documentation](./technologies.md)
4. Bắt đầu phát triển features mới

## Hỗ trợ

Nếu gặp vấn đề:
1. Kiểm tra logs trong console
2. Kiểm tra file `logs/spring-security-debug.log`
3. Xem documentation trong thư mục `docs/backend-docs`
4. Kiểm tra Swagger UI để xem API documentation

