package com.example.entitiesapp.mapper;

import com.example.entitiesapp.dto.UserDto;
import com.example.entitiesapp.model.User;
import org.mapstruct.Mapper;

@Mapper(componentModel = "spring")
public interface UserMapper extends BaseMapper<User, UserDto> {
} 