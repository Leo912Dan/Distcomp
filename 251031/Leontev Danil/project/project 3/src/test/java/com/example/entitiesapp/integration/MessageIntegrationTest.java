package com.example.entitiesapp.integration;

import com.example.entitiesapp.dto.MessageDto;
import com.example.entitiesapp.dto.TopicDto;
import com.example.entitiesapp.dto.UserDto;
import io.restassured.RestAssured;
import io.restassured.http.ContentType;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.boot.test.web.server.LocalServerPort;

import static io.restassured.RestAssured.given;
import static org.hamcrest.Matchers.*;

class MessageIntegrationTest extends BaseIntegrationTest {
    @LocalServerPort
    private int port;

    private Long topicId;

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

        Long userId = given()
                .contentType(ContentType.JSON)
                .body(userDto)
                .when()
                .post("/api/v1.0/users")
                .then()
                .statusCode(200)
                .extract()
                .path("id");

        // Create a topic
        TopicDto topicDto = new TopicDto();
        topicDto.setName("Test Topic");
        topicDto.setUserId(userId);

        topicId = given()
                .contentType(ContentType.JSON)
                .body(topicDto)
                .when()
                .post("/api/v1.0/topics")
                .then()
                .statusCode(200)
                .extract()
                .path("id");
    }

    @Test
    void testMessageCrudOperations() {
        // Create
        MessageDto messageDto = new MessageDto();
        messageDto.setContent("Test Message");
        messageDto.setTopicId(topicId);

        Long messageId = given()
                .contentType(ContentType.JSON)
                .body(messageDto)
                .when()
                .post("/api/v1.0/messages")
                .then()
                .statusCode(200)
                .body("id", notNullValue())
                .body("content", equalTo("Test Message"))
                .body("topicId", equalTo(topicId.intValue()))
                .extract()
                .path("id");

        // Get by id
        given()
                .when()
                .get("/api/v1.0/messages/" + messageId)
                .then()
                .statusCode(200)
                .body("id", equalTo(messageId.intValue()))
                .body("content", equalTo("Test Message"));

        // Update
        messageDto.setContent("Updated Message");
        given()
                .contentType(ContentType.JSON)
                .body(messageDto)
                .when()
                .put("/api/v1.0/messages/" + messageId)
                .then()
                .statusCode(200)
                .body("content", equalTo("Updated Message"));

        // Get all
        given()
                .when()
                .get("/api/v1.0/messages")
                .then()
                .statusCode(200)
                .body("content", hasSize(greaterThan(0)));

        // Get by topic id
        given()
                .when()
                .get("/api/v1.0/messages/topic/" + topicId)
                .then()
                .statusCode(200)
                .body("content", hasSize(greaterThan(0)));

        // Delete
        given()
                .when()
                .delete("/api/v1.0/messages/" + messageId)
                .then()
                .statusCode(200);

        // Verify deletion
        given()
                .when()
                .get("/api/v1.0/messages/" + messageId)
                .then()
                .statusCode(404);
    }
} 