package com.example.entitiesapp.service;

import com.example.entitiesapp.dto.TopicDto;
import com.example.entitiesapp.model.Topic;
import com.example.entitiesapp.repository.TopicRepository;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;

@Service
public class TopicService extends BaseServiceImpl<Topic, TopicDto> {
    public TopicService(TopicRepository repository, TopicMapper mapper) {
        super(repository, mapper);
    }

    public Page<TopicDto> getByUserId(Long userId, Pageable pageable) {
        return ((TopicRepository) repository).findByUserId(userId, pageable)
                .map(mapper::toDto);
    }
} 