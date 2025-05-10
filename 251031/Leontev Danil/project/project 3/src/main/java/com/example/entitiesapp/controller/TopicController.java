package com.example.entitiesapp.controller;

import com.example.entitiesapp.dto.TopicDto;
import com.example.entitiesapp.service.TopicService;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/v1.0/topics")
public class TopicController extends BaseControllerImpl<TopicDto> {
    private final TopicService topicService;

    public TopicController(TopicService service) {
        super(service);
        this.topicService = service;
    }

    @GetMapping("/user/{userId}")
    public ResponseEntity<Page<TopicDto>> getByUserId(@PathVariable Long userId, Pageable pageable) {
        return ResponseEntity.ok(topicService.getByUserId(userId, pageable));
    }
} 