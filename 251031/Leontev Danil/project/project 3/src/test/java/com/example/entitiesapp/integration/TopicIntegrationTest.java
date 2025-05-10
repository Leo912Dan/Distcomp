package com.example.entitiesapp.integration;

import com.example.entitiesapp.dto.TopicDto;
import com.example.entitiesapp.dto.UserDto;
import io.restassured.RestAssured;
import io.restassured.http.ContentType;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.boot.test.web.server.LocalServerPort;

import static io.restassured.RestAssured.given;
import static org.hamcrest.Matchers.*;

class TopicIntegrationTest extends BaseIntegrationTest {
    @LocalServerPort
    private int port;

    private Long userId;

    @BeforeEach
    void setUp() {
        RestAssured.port = port;
        RestAssured.baseURI = "http://localhost";

        // Create a user first
        UserDto userDto = new UserDto();
        userDto.setLogin("test");
        userDto.setPassword("password");
        userDto.setFirstName("John");
        userDto.setLastName("Doe");

        userId = given()
                .contentType(ContentType.JSON)
                .body(userDto)
                .when()
                .post("/api/v1.0/users")
                .then()
                .statusCode(200)
                .extract()
                .path("id");
    }

    @Test
    void testTopicCrudOperations() {
        // Create
        TopicDto topicDto = new TopicDto();
        topicDto.setName("Test Topic");
        topicDto.setUserId(userId);

        Long topicId = given()
                .contentType(ContentType.JSON)
                .body(topicDto)
                .when()
                .post("/api/v1.0/topics")
                .then()
                .statusCode(200)
                .body("id", notNullValue())
                .body("name", equalTo("Test Topic"))
                .body("userId", equalTo(userId.intValue()))
                .extract()
                .path("id");

        // Get by id
        given()
                .when()
                .get("/api/v1.0/topics/" + topicId)
                .then()
                .statusCode(200)
                .body("id", equalTo(topicId.intValue()))
                .body("name", equalTo("Test Topic"));

        // Update
        topicDto.setName("Updated Topic");
        given()
                .contentType(ContentType.JSON)
                .body(topicDto)
                .when()
                .put("/api/v1.0/topics/" + topicId)
                .then()
                .statusCode(200)
                .body("name", equalTo("Updated Topic"));

        // Get all
        given()
                .when()
                .get("/api/v1.0/topics")
                .then()
                .statusCode(200)
                .body("content", hasSize(greaterThan(0)));

        // Get by user id
        given()
                .when()
                .get("/api/v1.0/topics/user/" + userId)
                .then()
                .statusCode(200)
                .body("content", hasSize(greaterThan(0)));

        // Delete
        given()
                .when()
                .delete("/api/v1.0/topics/" + topicId)
                .then()
                .statusCode(200);

        // Verify deletion
        given()
                .when()
                .get("/api/v1.0/topics/" + topicId)
                .then()
                .statusCode(404);
    }
} 