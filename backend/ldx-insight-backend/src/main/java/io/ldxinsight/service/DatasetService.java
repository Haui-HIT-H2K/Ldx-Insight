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

import io.ldxinsight.dto.*;
import io.ldxinsight.model.Dataset;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;

import java.util.List;

public interface DatasetService {
    Page<DatasetDto> searchDatasets(String keyword, String category, Pageable pageable);

    DatasetDto getDatasetById(String id);
    DatasetDto createDataset(CreateDatasetRequest request);
    DatasetDto updateDataset(String id, CreateDatasetRequest request);
    void deleteDataset(String id);

    void incrementViewCount(String id);
    String getDownloadUrlAndIncrement(String id);

    StatSummaryDto getStatsSummary();

    List<String> getAllCategories();

    Page<DatasetDto> getDatasetsByCategory(String category, Pageable pageable);

    List<CategoryStatisDTO> getCategoryStats();
    List<DatasetDto> getTopViewedDatasets(int limit);
    List<DatasetDto> getTopDownloadedDatasets(int limit);
    String getDataUrl(String id);
}