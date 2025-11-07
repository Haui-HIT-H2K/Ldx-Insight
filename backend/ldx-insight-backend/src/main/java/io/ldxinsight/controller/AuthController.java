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

package io.ldxinsight.controller;

import io.ldxinsight.dto.AuthResponse;
import io.ldxinsight.dto.LoginRequest;
import io.ldxinsight.dto.RegisterRequest;
import io.ldxinsight.service.AuthService;
import io.ldxinsight.service.JwtCookieService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpCookie;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/v1/auth")
@RequiredArgsConstructor
@Tag(name = "3. Authentication API", description = "APIs Đăng ký, Đăng nhập và Đăng xuất")
public class AuthController {

    private final AuthService authService;
    private final JwtCookieService jwtCookieService;

    @Operation(summary = "Đăng ký tài khoản mới")
    @PostMapping("/register")
    public ResponseEntity<AuthResponse> register(
            @Valid @RequestBody RegisterRequest request,
            HttpServletResponse response
    ) {

        AuthResponse authResponse = authService.register(request);

        HttpCookie jwtCookie = jwtCookieService.createJwtCookie(authResponse.getToken());

        response.addHeader(HttpHeaders.SET_COOKIE, jwtCookie.toString());

        return ResponseEntity.ok(authResponse);
    }

    @Operation(summary = "Đăng nhập, lấy JWT Token (và set HttpOnly cookie)")
    @PostMapping("/login")
    public ResponseEntity<AuthResponse> login(
            @Valid @RequestBody LoginRequest request,
            HttpServletResponse response
    ) {
        // 1. Gọi service để đăng nhập và lấy token
        AuthResponse authResponse = authService.login(request);

        // 2. Tạo cookie bảo mật
        HttpCookie jwtCookie = jwtCookieService.createJwtCookie(authResponse.getToken());

        // 3. Set cookie vào response header
        response.addHeader(HttpHeaders.SET_COOKIE, jwtCookie.toString());

        // 4. Trả về JSON (để client biết đã thành công)
        return ResponseEntity.ok(authResponse);
    }


    @Operation(summary = "Đăng xuất (Xóa HttpOnly cookie)")
    @PostMapping("/logout")
    public ResponseEntity<?> logout() {
        // 1. Tạo một cookie "xóa" (rỗng, maxAge=0)
        HttpCookie clearCookie = jwtCookieService.clearJwtCookie();

        // 2. Set cookie đó vào header để xóa cookie cũ
        return ResponseEntity.ok()
                .header(HttpHeaders.SET_COOKIE, clearCookie.toString())
                .body("Logout successful!");
    }
}