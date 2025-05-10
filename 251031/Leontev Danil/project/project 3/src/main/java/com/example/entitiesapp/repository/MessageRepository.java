package com.example.entitiesapp.repository;

import com.example.entitiesapp.model.Message;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Repository;

@Repository
public interface MessageRepository extends BaseRepository<Message> {
    Page<Message> findByTopicId(Long topicId, Pageable pageable);
} 