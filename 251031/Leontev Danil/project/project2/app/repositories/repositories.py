from app.repositories.base_repository import BaseRepository
from app.models.entities import User, Topic, Mark, Message

class UserRepository(BaseRepository[User]):
    def __init__(self):
        super().__init__(User)

class TopicRepository(BaseRepository[Topic]):
    def __init__(self):
        super().__init__(Topic)

class MarkRepository(BaseRepository[Mark]):
    def __init__(self):
        super().__init__(Mark)

class MessageRepository(BaseRepository[Message]):
    def __init__(self):
        super().__init__(Message) 