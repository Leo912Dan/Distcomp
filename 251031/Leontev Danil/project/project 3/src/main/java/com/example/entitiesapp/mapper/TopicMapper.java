package com.example.entitiesapp.mapper;

import com.example.entitiesapp.dto.TopicDto;
import com.example.entitiesapp.model.Topic;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;

@Mapper(componentModel = "spring")
public interface TopicMapper extends BaseMapper<Topic, TopicDto> {
    @Mapping(target = "userId", source = "user.id")
    @Mapping(target = "markIds", expression = "java(entity.getMarks().stream().map(mark -> mark.getId()).collect(java.util.stream.Collectors.toList()))")
    TopicDto toDto(Topic entity);

    @Mapping(target = "user", ignore = true)
    @Mapping(target = "marks", ignore = true)
    Topic toEntity(TopicDto dto);
} 