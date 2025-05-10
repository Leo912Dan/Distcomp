package com.example.entitiesapp.service;

import com.example.entitiesapp.dto.MarkDto;
import com.example.entitiesapp.model.Mark;
import com.example.entitiesapp.repository.MarkRepository;
import org.springframework.stereotype.Service;

@Service
public class MarkService extends BaseServiceImpl<Mark, MarkDto> {
    public MarkService(MarkRepository repository, MarkMapper mapper) {
        super(repository, mapper);
    }
} 