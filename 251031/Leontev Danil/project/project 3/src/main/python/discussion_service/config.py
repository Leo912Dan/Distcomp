"""
Модуль конфигурации для Cassandra.
Содержит настройки подключения к базе данных и другие параметры.
"""

from pydantic_settings import BaseSettings

class CassandraSettings(BaseSettings):
    """
    Настройки подключения к Cassandra.
    
    Атрибуты:
        CASSANDRA_HOST: Хост Cassandra
        CASSANDRA_PORT: Порт Cassandra
        CASSANDRA_USER: Имя пользователя
        CASSANDRA_PASSWORD: Пароль
        CASSANDRA_KEYSPACE: Имя keyspace
    """
    # Настройки подключения к Cassandra
    CASSANDRA_HOST: str = "localhost"  # Хост по умолчанию
    CASSANDRA_PORT: int = 9042  # Стандартный порт Cassandra
    CASSANDRA_USER: str = "cassandra"  # Пользователь по умолчанию
    CASSANDRA_PASSWORD: str = "cassandra"  # Пароль по умолчанию
    CASSANDRA_KEYSPACE: str = "discussion"  # Имя keyspace для нашего приложения

    class Config:
        env_prefix = "CASSANDRA_"  # Префикс для переменных окружения

# Создаем экземпляр настроек
cassandra_settings = CassandraSettings() 