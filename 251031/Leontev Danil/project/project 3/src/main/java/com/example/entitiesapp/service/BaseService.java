package com.example.entitiesapp.service;

import com.example.entitiesapp.dto.BaseDto;
import com.example.entitiesapp.model.BaseEntity;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;

public interface BaseService<E extends BaseEntity, D extends BaseDto> {
    D create(D dto);
    D getById(Long id);
    Page<D> getAll(Pageable pageable);
    D update(Long id, D dto);
    void delete(Long id);
} 