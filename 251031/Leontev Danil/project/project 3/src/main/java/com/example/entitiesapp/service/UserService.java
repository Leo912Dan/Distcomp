package com.example.entitiesapp.service;

import com.example.entitiesapp.dto.UserDto;
import com.example.entitiesapp.model.User;
import com.example.entitiesapp.repository.UserRepository;
import org.springframework.stereotype.Service;

@Service
public class UserService extends BaseServiceImpl<User, UserDto> {
    public UserService(UserRepository repository, UserMapper mapper) {
        super(repository, mapper);
    }
} 