package com.example.entitiesapp.controller;

import com.example.entitiesapp.dto.MessageDto;
import com.example.entitiesapp.service.MessageService;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/v1.0/messages")
public class MessageController extends BaseControllerImpl<MessageDto> {
    private final MessageService messageService;

    public MessageController(MessageService service) {
        super(service);
        this.messageService = service;
    }

    @GetMapping("/topic/{topicId}")
    public ResponseEntity<Page<MessageDto>> getByTopicId(@PathVariable Long topicId, Pageable pageable) {
        return ResponseEntity.ok(messageService.getByTopicId(topicId, pageable));
    }
} 