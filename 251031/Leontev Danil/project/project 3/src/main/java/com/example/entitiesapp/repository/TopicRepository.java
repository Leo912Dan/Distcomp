package com.example.entitiesapp.repository;

import com.example.entitiesapp.model.Topic;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Repository;

@Repository
public interface TopicRepository extends BaseRepository<Topic> {
    Page<Topic> findByUserId(Long userId, Pageable pageable);
} 