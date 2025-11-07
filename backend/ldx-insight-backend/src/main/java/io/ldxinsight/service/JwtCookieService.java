/*
 * Copyright 2025 Haui.HIT - H2K
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package io.ldxinsight.service;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpCookie;
import org.springframework.http.ResponseCookie;
import org.springframework.stereotype.Service;

@Service
public class JwtCookieService {

    @Value("${jwt.cookie-name}")
    private String jwtCookieName;

    // Thời hạn 1 ngày (tính bằng giây), khớp với thời hạn của JWT
    private static final long JWT_EXPIRATION_SECONDS = 24 * 60 * 60;

    /**
     * Tạo một HttpOnly cookie chứa JWT.
     * Cookie này an toàn, JavaScript phía client không thể đọc được.
     */
    public HttpCookie createJwtCookie(String jwt) {
        return ResponseCookie.from(jwtCookieName, jwt)
                .httpOnly(true)     // <-- Quan trọng: Chống XSS
                .secure(true)       // <-- Quan trọng: Chỉ gửi qua HTTPS ý)
                .path("/") 
                .secure(true)             // Báo trình duyệt: Chỉ gửi cookie này qua HTTPS
                .sameSite("None")         // Cookie có hiệu lực trên toàn bộ domain
                .maxAge(JWT_EXPIRATION_SECONDS) // Thời gian sống (1 ngày)
                .domain("haui-hit-h2k.site")
                .build();
    }

    /**
     * Tạo một cookie "rỗng" (hết hạn ngay lập tức) để xóa cookie cũ
     * (dùng khi logout)
     */
    public HttpCookie clearJwtCookie() {
        return ResponseCookie.from(jwtCookieName, "")
                .httpOnly(true)
                .secure(true)
                .path("/")
                .secure(true)
                .sameSite("None")
                .maxAge(0)
                .domain("haui-hit-h2k.site")
                .build();
    }
}