package com.example.entitiesapp.controller;

import com.example.entitiesapp.dto.MarkDto;
import com.example.entitiesapp.service.MarkService;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/v1.0/marks")
public class MarkController extends BaseControllerImpl<MarkDto> {
    public MarkController(MarkService service) {
        super(service);
    }
} 