package com.example.entitiesapp.integration;

import com.example.entitiesapp.dto.MarkDto;
import io.restassured.RestAssured;
import io.restassured.http.ContentType;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.boot.test.web.server.LocalServerPort;

import static io.restassured.RestAssured.given;
import static org.hamcrest.Matchers.*;

class MarkIntegrationTest extends BaseIntegrationTest {
    @LocalServerPort
    private int port;

    @BeforeEach
    void setUp() {
        RestAssured.port = port;
        RestAssured.baseURI = "http://localhost";
    }

    @Test
    void testMarkCrudOperations() {
        // Create
        MarkDto markDto = new MarkDto();
        markDto.setName("Test Mark");

        Long markId = given()
                .contentType(ContentType.JSON)
                .body(markDto)
                .when()
                .post("/api/v1.0/marks")
                .then()
                .statusCode(200)
                .body("id", notNullValue())
                .body("name", equalTo("Test Mark"))
                .extract()
                .path("id");

        // Get by id
        given()
                .when()
                .get("/api/v1.0/marks/" + markId)
                .then()
                .statusCode(200)
                .body("id", equalTo(markId.intValue()))
                .body("name", equalTo("Test Mark"));

        // Update
        markDto.setName("Updated Mark");
        given()
                .contentType(ContentType.JSON)
                .body(markDto)
                .when()
                .put("/api/v1.0/marks/" + markId)
                .then()
                .statusCode(200)
                .body("name", equalTo("Updated Mark"));

        // Get all
        given()
                .when()
                .get("/api/v1.0/marks")
                .then()
                .statusCode(200)
                .body("content", hasSize(greaterThan(0)));

        // Delete
        given()
                .when()
                .delete("/api/v1.0/marks/" + markId)
                .then()
                .statusCode(200);

        // Verify deletion
        given()
                .when()
                .get("/api/v1.0/marks/" + markId)
                .then()
                .statusCode(404);
    }
} 