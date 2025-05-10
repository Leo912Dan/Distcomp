package com.example.entitiesapp.repository;

import com.example.entitiesapp.model.User;
import org.springframework.stereotype.Repository;

@Repository
public interface UserRepository extends BaseRepository<User> {
    boolean existsByLogin(String login);
} 