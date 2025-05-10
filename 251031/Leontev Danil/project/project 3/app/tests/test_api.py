import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db
from app.models import User, Topic, Message, Mark
from app.schemas import UserCreate, TopicCreate, MessageCreate, MarkCreate

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@db:5432/distcomp_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

# User Tests
class TestUserAPI:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.user_data = {
            "login": "testuser",
            "password": "testpass",
            "firstname": "Test",
            "lastname": "User"
        }
        yield
        db = TestingSessionLocal()
        db.query(User).delete()
        db.commit()
        db.close()

    def test_create_user(self):
        response = client.post("/users/", json=self.user_data)
        assert response.status_code == 200
        data = response.json()
        assert data["login"] == self.user_data["login"]
        assert data["firstname"] == self.user_data["firstname"]
        assert data["lastname"] == self.user_data["lastname"]

    def test_create_user_duplicate_login(self):
        client.post("/users/", json=self.user_data)
        response = client.post("/users/", json=self.user_data)
        assert response.status_code == 403

    def test_create_user_invalid_fields(self):
        invalid_data = self.user_data.copy()
        invalid_data["login"] = ""  # Пустой логин
        response = client.post("/users/", json=invalid_data)
        assert response.status_code == 422

# Topic Tests
class TestTopicAPI:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.user_data = {
            "login": "testuser",
            "password": "testpass",
            "firstname": "Test",
            "lastname": "User"
        }
        self.topic_data = {
            "title": "Test Topic",
            "content": "Test Content"
        }
        yield
        db = TestingSessionLocal()
        db.query(Topic).delete()
        db.query(User).delete()
        db.commit()
        db.close()

    def test_create_topic(self):
        user_response = client.post("/users/", json=self.user_data)
        user_id = user_response.json()["id"]
        
        self.topic_data["user_id"] = user_id
        response = client.post("/topics/", json=self.topic_data)
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == self.topic_data["title"]
        assert data["content"] == self.topic_data["content"]

    def test_create_topic_invalid_fields(self):
        invalid_data = self.topic_data.copy()
        invalid_data["title"] = ""  # Пустой заголовок
        response = client.post("/topics/", json=invalid_data)
        assert response.status_code == 422

    def test_create_topic_invalid_association(self):
        self.topic_data["user_id"] = 999  # Несуществующий пользователь
        response = client.post("/topics/", json=self.topic_data)
        assert response.status_code == 404

# Message Tests
class TestMessageAPI:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.user_data = {
            "login": "testuser",
            "password": "testpass",
            "firstname": "Test",
            "lastname": "User"
        }
        self.topic_data = {
            "title": "Test Topic",
            "content": "Test Content"
        }
        self.message_data = {
            "content": "Test Message"
        }
        yield
        db = TestingSessionLocal()
        db.query(Message).delete()
        db.query(Topic).delete()
        db.query(User).delete()
        db.commit()
        db.close()

    def test_create_message(self):
        user_response = client.post("/users/", json=self.user_data)
        user_id = user_response.json()["id"]
        
        self.topic_data["user_id"] = user_id
        topic_response = client.post("/topics/", json=self.topic_data)
        topic_id = topic_response.json()["id"]
        
        self.message_data["topic_id"] = topic_id
        self.message_data["user_id"] = user_id
        response = client.post("/messages/", json=self.message_data)
        assert response.status_code == 200
        data = response.json()
        assert data["content"] == self.message_data["content"]

    def test_create_message_invalid_fields(self):
        invalid_data = self.message_data.copy()
        invalid_data["content"] = ""  # Пустое сообщение
        response = client.post("/messages/", json=invalid_data)
        assert response.status_code == 422

# Mark Tests
class TestMarkAPI:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.user_data = {
            "login": "testuser",
            "password": "testpass",
            "firstname": "Test",
            "lastname": "User"
        }
        self.topic_data = {
            "title": "Test Topic",
            "content": "Test Content"
        }
        self.mark_data = {
            "name": "Test Mark"
        }
        yield
        db = TestingSessionLocal()
        db.query(Mark).delete()
        db.query(Topic).delete()
        db.query(User).delete()
        db.commit()
        db.close()

    def test_create_mark(self):
        user_response = client.post("/users/", json=self.user_data)
        user_id = user_response.json()["id"]
        
        self.topic_data["user_id"] = user_id
        topic_response = client.post("/topics/", json=self.topic_data)
        topic_id = topic_response.json()["id"]
        
        self.mark_data["topic_id"] = topic_id
        response = client.post("/marks/", json=self.mark_data)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == self.mark_data["name"]

    def test_create_mark_invalid_fields(self):
        invalid_data = self.mark_data.copy()
        invalid_data["name"] = ""  # Пустое имя
        response = client.post("/marks/", json=invalid_data)
        assert response.status_code == 422 