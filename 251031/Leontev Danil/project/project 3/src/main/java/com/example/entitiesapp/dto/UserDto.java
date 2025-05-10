package com.example.entitiesapp.dto;

import lombok.Data;

@Data
public class UserDto implements BaseDto {
    private Long id;
    private String login;
    private String password;
    private String firstName;
    private String lastName;
} 