package com.example.entitiesapp.mapper;

import com.example.entitiesapp.dto.MessageDto;
import com.example.entitiesapp.model.Message;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;

@Mapper(componentModel = "spring")
public interface MessageMapper extends BaseMapper<Message, MessageDto> {
    @Mapping(target = "topicId", source = "topic.id")
    MessageDto toDto(Message entity);

    @Mapping(target = "topic", ignore = true)
    Message toEntity(MessageDto dto);
} 