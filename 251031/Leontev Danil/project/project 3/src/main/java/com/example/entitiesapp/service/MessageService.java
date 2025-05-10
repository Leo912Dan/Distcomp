package com.example.entitiesapp.service;

import com.example.entitiesapp.dto.MessageDto;
import com.example.entitiesapp.model.Message;
import com.example.entitiesapp.repository.MessageRepository;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;

@Service
public class MessageService extends BaseServiceImpl<Message, MessageDto> {
    public MessageService(MessageRepository repository, MessageMapper mapper) {
        super(repository, mapper);
    }

    public Page<MessageDto> getByTopicId(Long topicId, Pageable pageable) {
        return ((MessageRepository) repository).findByTopicId(topicId, pageable)
                .map(mapper::toDto);
    }
} 