/**
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

export type SuccessMessageResponse = 'success';
export type ErrorMessageResponse = 'error';
export type MessageResponse = SuccessMessageResponse | ErrorMessageResponse;

export interface ApiResponse<T = any> {
  code: number;
  message: MessageResponse;
  data: T;
  error: string;
}

export interface ApiErrorResponse {
  code: number;
  message: string;
  stack?: string;
}
