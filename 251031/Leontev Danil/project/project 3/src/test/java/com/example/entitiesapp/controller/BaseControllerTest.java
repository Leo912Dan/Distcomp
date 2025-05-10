package com.example.entitiesapp.controller;

import com.example.entitiesapp.dto.BaseDto;
import com.example.entitiesapp.service.BaseService;
import org.junit.jupiter.api.BeforeEach;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageImpl;
import org.springframework.data.domain.Pageable;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.setup.MockMvcBuilders;

import java.util.Collections;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;

public abstract class BaseControllerTest<D extends BaseDto> {
    protected MockMvc mockMvc;

    @Mock
    protected BaseService<?, D> service;

    @BeforeEach
    void setUp() {
        MockitoAnnotations.openMocks(this);
        mockMvc = MockMvcBuilders.standaloneSetup(getController())
                .build();
    }

    protected abstract Object getController();

    protected void mockServiceMethods(D dto) {
        when(service.create(any())).thenReturn(dto);
        when(service.getById(any())).thenReturn(dto);
        when(service.update(any(), any())).thenReturn(dto);
        Page<D> page = new PageImpl<>(Collections.singletonList(dto));
        when(service.getAll(any(Pageable.class))).thenReturn(page);
    }
} 