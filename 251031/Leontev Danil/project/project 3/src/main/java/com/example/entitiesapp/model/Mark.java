package com.example.entitiesapp.model;

import jakarta.persistence.*;
import lombok.Data;
import lombok.EqualsAndHashCode;

import java.util.ArrayList;
import java.util.List;

@Entity
@Table(name = "tbl_mark")
@Data
@EqualsAndHashCode(callSuper = false)
public class Mark implements BaseEntity {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String name;

    @ManyToMany(mappedBy = "marks")
    private List<Topic> topics = new ArrayList<>();
} 