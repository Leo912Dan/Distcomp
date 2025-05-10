package com.example.entitiesapp.controller;

import com.example.entitiesapp.dto.BaseDto;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.http.ResponseEntity;

public interface BaseController<D extends BaseDto> {
    ResponseEntity<D> create(D dto);
    ResponseEntity<D> getById(Long id);
    ResponseEntity<Page<D>> getAll(Pageable pageable);
    ResponseEntity<D> update(Long id, D dto);
    ResponseEntity<Void> delete(Long id);
} 