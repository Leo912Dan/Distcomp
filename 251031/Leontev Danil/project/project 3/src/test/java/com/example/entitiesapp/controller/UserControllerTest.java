package com.example.entitiesapp.controller;

import com.example.entitiesapp.dto.UserDto;
import com.example.entitiesapp.service.UserService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

class UserControllerTest extends BaseControllerTest<UserDto> {
    private UserController controller;
    private UserDto userDto;

    @BeforeEach
    void setUp() {
        super.setUp();
        controller = new UserController((UserService) service);
        userDto = new UserDto();
        userDto.setId(1L);
        userDto.setLogin("test");
        userDto.setPassword("password");
        userDto.setFirstName("John");
        userDto.setLastName("Doe");
        mockServiceMethods(userDto);
    }

    @Override
    protected Object getController() {
        return controller;
    }

    @Test
    void create() throws Exception {
        mockMvc.perform(MockMvcRequestBuilders.post("/api/v1.0/users")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{\"login\":\"test\",\"password\":\"password\",\"firstName\":\"John\",\"lastName\":\"Doe\"}"))
                .andExpect(status().isOk());
    }

    @Test
    void getById() throws Exception {
        mockMvc.perform(MockMvcRequestBuilders.get("/api/v1.0/users/1"))
                .andExpect(status().isOk());
    }

    @Test
    void getAll() throws Exception {
        mockMvc.perform(MockMvcRequestBuilders.get("/api/v1.0/users"))
                .andExpect(status().isOk());
    }

    @Test
    void update() throws Exception {
        mockMvc.perform(MockMvcRequestBuilders.put("/api/v1.0/users/1")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{\"login\":\"test\",\"password\":\"password\",\"firstName\":\"John\",\"lastName\":\"Doe\"}"))
                .andExpect(status().isOk());
    }

    @Test
    void delete() throws Exception {
        mockMvc.perform(MockMvcRequestBuilders.delete("/api/v1.0/users/1"))
                .andExpect(status().isOk());
    }
} 