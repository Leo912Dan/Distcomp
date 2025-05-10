package com.example.entitiesapp.mapper;

import com.example.entitiesapp.dto.BaseDto;
import com.example.entitiesapp.model.BaseEntity;

public interface BaseMapper<E extends BaseEntity, D extends BaseDto> {
    D toDto(E entity);
    E toEntity(D dto);
} 