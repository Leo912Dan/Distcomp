from fastapi import HTTPException, status
from datetime import datetime
from app.models import (
    User, Topic, Mark, Message,
    UserRequestTo, UserResponseTo,
    TopicRequestTo, TopicResponseTo, TopicUpdateTo,
    MarkRequestTo, MarkResponseTo, MarkUpdateTo,
    MessageRequestTo, MessageResponseTo, MessageUpdateTo
)
from app.repositories import InMemoryRepository

# Инициализация репозиториев для хранения данных
# InMemoryRepository - простая реализация хранилища в памяти
user_repo = InMemoryRepository[User]()
topic_repo = InMemoryRepository[Topic]()
mark_repo = InMemoryRepository[Mark]()
message_repo = InMemoryRepository[Message]()

# ----- User Service -----
class UserService:
    """Сервис для работы с пользователями"""
    
    @staticmethod
    def create(dto: UserRequestTo) -> UserResponseTo:
        """Создание нового пользователя"""
        user = User(
            id=0,  # ID будет назначен репозиторием
            login=dto.login,
            password=dto.password,
            firstname=dto.firstname,
            lastname=dto.lastname
        )
        user = user_repo.create(user)
        return UserResponseTo(**user.model_dump())

    @staticmethod
    def get_by_id(id: int) -> UserResponseTo:
        """Получение пользователя по ID"""
        user = user_repo.find_by_id(id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return UserResponseTo(**user.model_dump())

    @staticmethod
    def get_all() -> list[UserResponseTo]:
        """Получение списка всех пользователей"""
        return [UserResponseTo(**u.model_dump()) for u in user_repo.find_all()]

    @staticmethod
    def update(dto: UserResponseTo) -> UserResponseTo:
        """Обновление данных пользователя"""
        if not user_repo.find_by_id(dto.id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        user = User(
            id=dto.id,
            login=dto.login,
            password=dto.password,
            firstname=dto.firstname,
            lastname=dto.lastname
        )
        updated = user_repo.update(dto.id, user)
        return UserResponseTo(**updated.model_dump())

    @staticmethod
    def delete(id: int) -> None:
        """Удаление пользователя"""
        print(f"Trying to delete user with id {id}")
        result = user_repo.delete(id)
        print(f"Delete result: {result}")
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    @staticmethod
    def get_by_topic_id(topic_id: int) -> UserResponseTo:
        """Получение пользователя по ID темы (связь один-ко-многим)"""
        topic = topic_repo.find_by_id(topic_id)
        if not topic:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Topic not found")
        user = user_repo.find_by_id(topic.user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return UserResponseTo(**user.model_dump())

# ----- Topic Service -----
class TopicService:
    """Сервис для работы с темами"""
    
    @staticmethod
    def create(dto: TopicRequestTo) -> TopicResponseTo:
        """Создание новой темы"""
        # Проверяем существование пользователя
        user = user_repo.find_by_id(dto.user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
            
        topic = Topic(
            user_id=dto.user_id,
            title=dto.title,
            content=dto.content,
            created=datetime.now(),
            modified=datetime.now()
        )
        topic = topic_repo.create(topic)
        return TopicResponseTo(**topic.model_dump())

    @staticmethod
    def get_by_id(id: int) -> TopicResponseTo:
        """Получение темы по ID"""
        topic = topic_repo.find_by_id(id)
        if not topic:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Topic not found")
        return TopicResponseTo(**topic.model_dump())

    @staticmethod
    def get_all() -> list[TopicResponseTo]:
        """Получение списка всех тем"""
        return [TopicResponseTo(**t.model_dump()) for t in topic_repo.find_all()]

    @staticmethod
    def update(id: int, dto: TopicRequestTo) -> TopicResponseTo:
        """Обновление данных темы"""
        topic = Topic(
            id=id,
            user_id=dto.user_id,
            title=dto.title,
            content=dto.content,
            created=datetime.now(),
            modified=datetime.now()
        )
        updated = topic_repo.update(id, topic)
        if not updated:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Topic not found")
        return TopicResponseTo(**updated.model_dump())

    @staticmethod
    def delete(id: int) -> None:
        """Удаление темы"""
        if not topic_repo.delete(id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Topic not found")

    @staticmethod
    def search(**kwargs) -> TopicResponseTo:
        """Поиск тем по параметрам"""
        for topic in topic_repo.find_all():
            match = True
            for key, value in kwargs.items():
                if value is not None and getattr(topic, key, None) != value:
                    match = False
                    break
            if match:
                return TopicResponseTo(**topic.model_dump())
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Topic not found")

# ----- Mark Service -----
class MarkService:
    """Сервис для работы с метками"""
    
    @staticmethod
    def create(dto: MarkRequestTo) -> MarkResponseTo:
        """Создание новой метки"""
        mark = Mark(
            id=0,
            name=dto.name
        )
        mark = mark_repo.create(mark)
        return MarkResponseTo(**mark.model_dump())

    @staticmethod
    def get_by_id(id: int) -> MarkResponseTo:
        """Получение метки по ID"""
        mark = mark_repo.find_by_id(id)
        if not mark:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mark not found")
        return MarkResponseTo(**mark.model_dump())

    @staticmethod
    def get_all() -> list[MarkResponseTo]:
        """Получение списка всех меток"""
        return [MarkResponseTo(**m.model_dump()) for m in mark_repo.find_all()]

    @staticmethod
    def update(id: int, dto: MarkRequestTo) -> MarkResponseTo:
        """Обновление данных метки"""
        mark = Mark(
            id=id,
            name=dto.name
        )
        updated = mark_repo.update(id, mark)
        if not updated:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mark not found")
        return MarkResponseTo(**updated.model_dump())

    @staticmethod
    def delete(id: int) -> None:
        """Удаление метки"""
        if not mark_repo.delete(id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mark not found")

    @staticmethod
    def get_by_topic_id(topic_id: int) -> list[MarkResponseTo]:
        """Получение меток по ID темы (связь многие-ко-многим)"""
        # Здесь должна быть реализована связь многие-ко-многим Topic-Mark
        # Пока возвращаем пустой список (реализовать позже)
        return []

# ----- Message Service -----
class MessageService:
    """Сервис для работы с сообщениями"""
    
    @staticmethod
    def create(dto: MessageRequestTo) -> MessageResponseTo:
        """Создание нового сообщения"""
        # Проверяем существование топика
        topic = topic_repo.find_by_id(dto.topic_id)
        if not topic:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Topic not found")
            
        message = Message(
            id=0,
            topic_id=dto.topic_id,
            content=dto.content
        )
        message = message_repo.create(message)
        return MessageResponseTo(**message.model_dump())

    @staticmethod
    def get_by_id(id: int) -> MessageResponseTo:
        """Получение сообщения по ID"""
        message = message_repo.find_by_id(id)
        if not message:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found")
        return MessageResponseTo(**message.model_dump())

    @staticmethod
    def get_all() -> list[MessageResponseTo]:
        """Получение списка всех сообщений"""
        return [MessageResponseTo(**m.model_dump()) for m in message_repo.find_all()]

    @staticmethod
    def update(id: int, dto: MessageRequestTo) -> MessageResponseTo:
        """Обновление данных сообщения"""
        message = Message(
            id=id,
            topic_id=dto.topic_id,
            content=dto.content
        )
        updated = message_repo.update(id, message)
        if not updated:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found")
        return MessageResponseTo(**updated.model_dump())

    @staticmethod
    def delete(id: int) -> None:
        """Удаление сообщения"""
        if not message_repo.delete(id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found")

    @staticmethod
    def get_by_topic_id(topic_id: int) -> list[MessageResponseTo]:
        """Получение сообщений по ID темы (связь один-ко-многим)"""
        messages = [m for m in message_repo.find_all() if m.topic_id == topic_id]
        return [MessageResponseTo(**m.model_dump()) for m in messages]