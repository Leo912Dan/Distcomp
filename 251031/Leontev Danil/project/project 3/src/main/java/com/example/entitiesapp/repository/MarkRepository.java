package com.example.entitiesapp.repository;

import com.example.entitiesapp.model.Mark;
import org.springframework.stereotype.Repository;

@Repository
public interface MarkRepository extends BaseRepository<Mark> {
    boolean existsByName(String name);
} 