package com.example.entitiesapp.controller;

import com.example.entitiesapp.dto.MessageDto;
import com.example.entitiesapp.service.MessageService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageImpl;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

import java.time.LocalDateTime;
import java.util.Collections;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyLong;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

class MessageControllerTest extends BaseControllerTest<MessageDto> {
    private MessageController controller;
    private MessageDto messageDto;

    @BeforeEach
    void setUp() {
        super.setUp();
        controller = new MessageController((MessageService) service);
        messageDto = new MessageDto();
        messageDto.setId(1L);
        messageDto.setContent("Test Message");
        messageDto.setTopicId(1L);
        messageDto.setCreatedAt(LocalDateTime.now());
        mockServiceMethods(messageDto);
    }

    @Override
    protected Object getController() {
        return controller;
    }

    @Test
    void create() throws Exception {
        mockMvc.perform(MockMvcRequestBuilders.post("/api/v1.0/messages")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{\"content\":\"Test Message\",\"topicId\":1}"))
                .andExpect(status().isOk());
    }

    @Test
    void getById() throws Exception {
        mockMvc.perform(MockMvcRequestBuilders.get("/api/v1.0/messages/1"))
                .andExpect(status().isOk());
    }

    @Test
    void getAll() throws Exception {
        mockMvc.perform(MockMvcRequestBuilders.get("/api/v1.0/messages"))
                .andExpect(status().isOk());
    }

    @Test
    void update() throws Exception {
        mockMvc.perform(MockMvcRequestBuilders.put("/api/v1.0/messages/1")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{\"content\":\"Test Message\",\"topicId\":1}"))
                .andExpect(status().isOk());
    }

    @Test
    void delete() throws Exception {
        mockMvc.perform(MockMvcRequestBuilders.delete("/api/v1.0/messages/1"))
                .andExpect(status().isOk());
    }

    @Test
    void getByTopicId() throws Exception {
        Page<MessageDto> page = new PageImpl<>(Collections.singletonList(messageDto));
        when(((MessageService) service).getByTopicId(anyLong(), any())).thenReturn(page);

        mockMvc.perform(MockMvcRequestBuilders.get("/api/v1.0/messages/topic/1"))
                .andExpect(status().isOk());
    }
} 