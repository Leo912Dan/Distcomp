package com.example.entitiesapp.dto;

import lombok.Data;

import java.time.LocalDateTime;

@Data
public class MessageDto implements BaseDto {
    private Long id;
    private String content;
    private Long topicId;
    private LocalDateTime createdAt;
} 