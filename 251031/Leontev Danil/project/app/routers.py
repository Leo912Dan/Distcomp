from fastapi import APIRouter, HTTPException, status
from typing import Union
from app.models import (
    UserRequestTo, UserResponseTo,
    TopicRequestTo, TopicResponseTo, TopicUpdateTo,
    MessageRequestTo, MessageResponseTo, MessageUpdateTo,
    MarkRequestTo, MarkResponseTo, MarkUpdateTo
)
from app.services import UserService, TopicService, MarkService, MessageService

# Создаем роутер с префиксом /api/v1.0
# Это позволяет версионировать API и легко добавлять новые версии
router = APIRouter(prefix="/api/v1.0")

# ----- User Endpoints -----
# Создание нового пользователя
@router.post("/users", response_model=UserResponseTo, status_code=status.HTTP_201_CREATED)
def create_user(dto: UserRequestTo):
    return UserService.create(dto)

# Получение списка всех пользователей
@router.get("/users", response_model=list[UserResponseTo], status_code=status.HTTP_200_OK)
def get_all_users():
    try:
        return UserService.get_all()
    except Exception:
        return []

# Получение пользователя по ID
@router.get("/users/{id}", response_model=UserResponseTo, status_code=status.HTTP_200_OK)
def get_user(id: str):
    try:
        int_id = int(id)
        return UserService.get_by_id(int_id)
    except Exception:
        return UserResponseTo(id=0, login="", password="", firstname="", lastname="")

# Обновление пользователя
@router.put("/users", response_model=UserResponseTo, status_code=status.HTTP_200_OK)
def update_user(dto: UserResponseTo):
    return UserService.update(dto)

# Удаление пользователя
@router.delete("/users/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: str):
    print(f"Deleting user with id {id}")
    try:
        int_id = int(id)
    except ValueError:
        print("Invalid ID format")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid user ID format")
    
    try:
        UserService.delete(int_id)
    except Exception as e:
        print(f"Error deleting user: {str(e)}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

# Получение пользователя по ID темы (связь один-ко-многим)
@router.get("/users/topic/{topic_id}", response_model=UserResponseTo, status_code=status.HTTP_200_OK)
def get_user_by_topic(topic_id: int):
    return UserService.get_by_topic_id(topic_id)

# ----- Topic Endpoints -----
# Создание новой темы
@router.post("/topics", response_model=TopicResponseTo, status_code=status.HTTP_201_CREATED)
def create_topic(dto: TopicRequestTo):
    return TopicService.create(dto)

# Получение списка всех тем
@router.get("/topics", response_model=list[TopicResponseTo], status_code=status.HTTP_200_OK)
def get_all_topics():
    return TopicService.get_all()

# Получение темы по ID
@router.get("/topics/{id}", response_model=TopicResponseTo, status_code=status.HTTP_200_OK)
def get_topic(id: int):
    return TopicService.get_by_id(id)

# Обновление темы
@router.put("/topics", response_model=TopicResponseTo, status_code=status.HTTP_200_OK)
def update_topic(dto: TopicUpdateTo):
    try:
        numeric_id = int(dto.id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Topic not found")
    update_dto = TopicRequestTo(
        user_id=dto.user_id,
        title=dto.title,
        content=dto.content
    )
    return TopicService.update(numeric_id, update_dto)

# Удаление темы
@router.delete("/topics/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_topic(id: int):
    return TopicService.delete(id)

# Поиск тем по параметрам
@router.get("/topics/search", response_model=TopicResponseTo, status_code=status.HTTP_200_OK)
def search_topic(user_id: Union[int, None] = None, title: Union[str, None] = None, content: Union[str, None] = None):
    search_params = {"user_id": user_id, "title": title, "content": content}
    return TopicService.search(**search_params)

# ----- Message Endpoints -----
# Создание нового сообщения
@router.post("/messages", response_model=MessageResponseTo, status_code=status.HTTP_201_CREATED)
def create_message(dto: MessageRequestTo):
    return MessageService.create(dto)

# Получение списка всех сообщений
@router.get("/messages", response_model=list[MessageResponseTo], status_code=status.HTTP_200_OK)
def get_all_messages():
    return MessageService.get_all()

# Получение сообщения по ID
@router.get("/messages/{id}", response_model=MessageResponseTo, status_code=status.HTTP_200_OK)
def get_message(id: int):
    return MessageService.get_by_id(id)

# Обновление сообщения
@router.put("/messages", response_model=MessageResponseTo, status_code=status.HTTP_200_OK)
def update_message(dto: MessageUpdateTo):
    try:
        numeric_id = int(dto.id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Message not found")
    update_dto = MessageRequestTo(
        topic_id=dto.topic_id,
        content=dto.content
    )
    return MessageService.update(numeric_id, update_dto)

# Удаление сообщения
@router.delete("/messages/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_message(id: str):
    try:
        int_id = int(id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid message ID format")
    return MessageService.delete(int_id)

# Получение сообщений по ID темы (связь один-ко-многим)
@router.get("/messages/topic/{topic_id}", response_model=list[MessageResponseTo], status_code=status.HTTP_200_OK)
def get_messages_by_topic(topic_id: int):
    return MessageService.get_by_topic_id(topic_id)

# ----- Mark Endpoints -----
# Создание новой метки
@router.post("/marks", response_model=MarkResponseTo, status_code=status.HTTP_201_CREATED)
def create_mark(dto: MarkRequestTo):
    return MarkService.create(dto)

# Получение списка всех меток
@router.get("/marks", response_model=list[MarkResponseTo], status_code=status.HTTP_200_OK)
def get_all_marks():
    return MarkService.get_all()

# Получение метки по ID
@router.get("/marks/{id}", response_model=MarkResponseTo, status_code=status.HTTP_200_OK)
def get_mark(id: int):
    return MarkService.get_by_id(id)

# Обновление метки
@router.put("/marks", response_model=MarkResponseTo, status_code=status.HTTP_200_OK)
def update_mark(dto: MarkUpdateTo):
    return MarkService.update(dto.id, MarkRequestTo(name=dto.name))

# Удаление метки
@router.delete("/marks/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_mark(id: int):
    return MarkService.delete(id)

# Получение меток по ID темы (связь многие-ко-многим)
@router.get("/marks/topic/{topic_id}", response_model=list[MarkResponseTo], status_code=status.HTTP_200_OK)
def get_marks_by_topic(topic_id: int):
    return MarkService.get_by_topic_id(topic_id)