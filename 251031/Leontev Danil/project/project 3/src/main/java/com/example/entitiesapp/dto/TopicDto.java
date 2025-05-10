package com.example.entitiesapp.dto;

import lombok.Data;

import java.util.List;

@Data
public class TopicDto implements BaseDto {
    private Long id;
    private String name;
    private Long userId;
    private List<Long> markIds;
} 