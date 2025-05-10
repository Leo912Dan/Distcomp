package com.example.entitiesapp.controller;

import com.example.entitiesapp.dto.TopicDto;
import com.example.entitiesapp.service.TopicService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageImpl;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

import java.util.Collections;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyLong;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

class TopicControllerTest extends BaseControllerTest<TopicDto> {
    private TopicController controller;
    private TopicDto topicDto;

    @BeforeEach
    void setUp() {
        super.setUp();
        controller = new TopicController((TopicService) service);
        topicDto = new TopicDto();
        topicDto.setId(1L);
        topicDto.setName("Test Topic");
        topicDto.setUserId(1L);
        mockServiceMethods(topicDto);
    }

    @Override
    protected Object getController() {
        return controller;
    }

    @Test
    void create() throws Exception {
        mockMvc.perform(MockMvcRequestBuilders.post("/api/v1.0/topics")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{\"name\":\"Test Topic\",\"userId\":1}"))
                .andExpect(status().isOk());
    }

    @Test
    void getById() throws Exception {
        mockMvc.perform(MockMvcRequestBuilders.get("/api/v1.0/topics/1"))
                .andExpect(status().isOk());
    }

    @Test
    void getAll() throws Exception {
        mockMvc.perform(MockMvcRequestBuilders.get("/api/v1.0/topics"))
                .andExpect(status().isOk());
    }

    @Test
    void update() throws Exception {
        mockMvc.perform(MockMvcRequestBuilders.put("/api/v1.0/topics/1")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{\"name\":\"Test Topic\",\"userId\":1}"))
                .andExpect(status().isOk());
    }

    @Test
    void delete() throws Exception {
        mockMvc.perform(MockMvcRequestBuilders.delete("/api/v1.0/topics/1"))
                .andExpect(status().isOk());
    }

    @Test
    void getByUserId() throws Exception {
        Page<TopicDto> page = new PageImpl<>(Collections.singletonList(topicDto));
        when(((TopicService) service).getByUserId(anyLong(), any())).thenReturn(page);

        mockMvc.perform(MockMvcRequestBuilders.get("/api/v1.0/topics/user/1"))
                .andExpect(status().isOk());
    }
} 