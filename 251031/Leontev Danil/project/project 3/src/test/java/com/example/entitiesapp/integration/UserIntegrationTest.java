package com.example.entitiesapp.integration;

import com.example.entitiesapp.dto.UserDto;
import io.restassured.RestAssured;
import io.restassured.http.ContentType;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.boot.test.web.server.LocalServerPort;

import static io.restassured.RestAssured.given;
import static org.hamcrest.Matchers.*;

class UserIntegrationTest extends BaseIntegrationTest {
    @LocalServerPort
    private int port;

    @BeforeEach
    void setUp() {
        RestAssured.port = port;
        RestAssured.baseURI = "http://localhost";
    }

    @Test
    void testUserCrudOperations() {
        // Create
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
                .body("id", notNullValue())
                .body("login", equalTo("test"))
                .body("firstName", equalTo("John"))
                .body("lastName", equalTo("Doe"))
                .extract()
                .path("id");

        // Get by id
        given()
                .when()
                .get("/api/v1.0/users/" + userId)
                .then()
                .statusCode(200)
                .body("id", equalTo(userId.intValue()))
                .body("login", equalTo("test"));

        // Update
        userDto.setFirstName("Jane");
        given()
                .contentType(ContentType.JSON)
                .body(userDto)
                .when()
                .put("/api/v1.0/users/" + userId)
                .then()
                .statusCode(200)
                .body("firstName", equalTo("Jane"));

        // Get all
        given()
                .when()
                .get("/api/v1.0/users")
                .then()
                .statusCode(200)
                .body("content", hasSize(greaterThan(0)));

        // Delete
        given()
                .when()
                .delete("/api/v1.0/users/" + userId)
                .then()
                .statusCode(200);

        // Verify deletion
        given()
                .when()
                .get("/api/v1.0/users/" + userId)
                .then()
                .statusCode(404);
    }
} 