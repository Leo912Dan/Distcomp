package com.example.entitiesapp.mapper;

import com.example.entitiesapp.dto.MarkDto;
import com.example.entitiesapp.model.Mark;
import org.mapstruct.Mapper;

@Mapper(componentModel = "spring")
public interface MarkMapper extends BaseMapper<Mark, MarkDto> {
} 