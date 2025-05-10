import json
from typing import Any, Optional, List, Dict
import redis
from app.config import settings
from datetime import timedelta

class RedisCache:
    def __init__(self):
        self.redis_client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            password=settings.REDIS_PASSWORD,
            decode_responses=True
        )
        
        # Время жизни кеша по умолчанию
        self.DEFAULT_TTL = 3600  # 1 час
        
        # Префиксы для разных типов данных
        self.USER_PREFIX = "user:"
        self.TOPIC_PREFIX = "topic:"
        self.MARK_PREFIX = "mark:"
        self.MESSAGE_PREFIX = "message:"
    
    def _get_key(self, prefix: str, id: Any) -> str:
        """Создать ключ для кеша"""
        return f"{prefix}{id}"
    
    def get(self, key: str) -> Optional[Any]:
        """Получить значение из кеша"""
        value = self.redis_client.get(key)
        if value:
            return json.loads(value)
        return None
    
    def set(self, key: str, value: Any, expire: int = None) -> None:
        """Установить значение в кеш"""
        if expire is None:
            expire = self.DEFAULT_TTL
        self.redis_client.setex(
            key,
            expire,
            json.dumps(value)
        )
    
    def delete(self, key: str) -> None:
        """Удалить значение из кеша"""
        self.redis_client.delete(key)
    
    def clear(self) -> None:
        """Очистить весь кеш"""
        self.redis_client.flushdb()
    
    # Методы для работы с пользователями
    def get_user(self, user_id: int) -> Optional[Dict]:
        """Получить пользователя из кеша"""
        return self.get(self._get_key(self.USER_PREFIX, user_id))
    
    def set_user(self, user_id: int, user_data: Dict) -> None:
        """Сохранить пользователя в кеш"""
        self.set(self._get_key(self.USER_PREFIX, user_id), user_data)
    
    def delete_user(self, user_id: int) -> None:
        """Удалить пользователя из кеша"""
        self.delete(self._get_key(self.USER_PREFIX, user_id))
    
    # Методы для работы с темами
    def get_topic(self, topic_id: int) -> Optional[Dict]:
        """Получить тему из кеша"""
        return self.get(self._get_key(self.TOPIC_PREFIX, topic_id))
    
    def set_topic(self, topic_id: int, topic_data: Dict) -> None:
        """Сохранить тему в кеш"""
        self.set(self._get_key(self.TOPIC_PREFIX, topic_id), topic_data)
    
    def delete_topic(self, topic_id: int) -> None:
        """Удалить тему из кеша"""
        self.delete(self._get_key(self.TOPIC_PREFIX, topic_id))
    
    # Методы для работы с оценками
    def get_mark(self, mark_id: int) -> Optional[Dict]:
        """Получить оценку из кеша"""
        return self.get(self._get_key(self.MARK_PREFIX, mark_id))
    
    def set_mark(self, mark_id: int, mark_data: Dict) -> None:
        """Сохранить оценку в кеш"""
        self.set(self._get_key(self.MARK_PREFIX, mark_id), mark_data)
    
    def delete_mark(self, mark_id: int) -> None:
        """Удалить оценку из кеша"""
        self.delete(self._get_key(self.MARK_PREFIX, mark_id))
    
    def get_topic_marks(self, topic_id: int) -> List[Dict]:
        """Получить все оценки для темы"""
        pattern = f"{self.MARK_PREFIX}*"
        keys = self.redis_client.keys(pattern)
        marks = []
        for key in keys:
            mark = self.get(key)
            if mark and mark.get('topic_id') == topic_id:
                marks.append(mark)
        return marks
    
    def invalidate_topic_marks(self, topic_id: int) -> None:
        """Инвалидировать все оценки для темы"""
        marks = self.get_topic_marks(topic_id)
        for mark in marks:
            self.delete_mark(mark['id'])

# Создаем глобальный экземпляр кеша
cache = RedisCache() 