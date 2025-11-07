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

package io.ldxinsight.repository;

import io.ldxinsight.dto.CategoryStatisDTO;
import io.ldxinsight.model.Dataset;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.data.mongodb.repository.Query;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface DatasetRepository extends MongoRepository<Dataset, String> {

    Page<Dataset> findByTitleContainingIgnoreCaseOrDescriptionContainingIgnoreCase(
            String titleKeyword, String descriptionKeyword, Pageable pageable
    );

    Page<Dataset> findByCategoryIgnoreCase(String category, Pageable pageable);

    long countByCategoryIgnoreCase(String category);

    @Query("SELECT new io.ldxinsight.dto.CategoryStatDto(d.category, COUNT(d.id)) " +
           "FROM Dataset d " +
           "GROUP BY d.category " +
           "ORDER BY COUNT(d.id) DESC")
    List<CategoryStatisDTO> countDatasetsByCategory();

    Page<Dataset> findByOrderByViewCountDesc(Pageable pageable);

    Page<Dataset> findByOrderByDownloadCountDesc(Pageable pageable);
}