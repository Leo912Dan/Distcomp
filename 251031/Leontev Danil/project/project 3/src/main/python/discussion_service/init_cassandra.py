"""
Модуль инициализации подключения к Cassandra.
Содержит функции для установки соединения с базой данных и создания необходимых таблиц.
"""

import logging
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.cqlengine import connection
from cassandra.cqlengine.management import sync_table

from .models import Message
from .config import cassandra_settings

logger = logging.getLogger(__name__)

def init_cassandra():
    """
    Инициализирует подключение к Cassandra и создает необходимые таблицы.
    
    Процесс инициализации:
    1. Создает кластер Cassandra
    2. Устанавливает соединение
    3. Создает keyspace если не существует
    4. Синхронизирует модели с таблицами
    """
    try:
        # Создаем кластер Cassandra с указанными настройками
        cluster = Cluster(
            [cassandra_settings.CASSANDRA_HOST],
            port=cassandra_settings.CASSANDRA_PORT,
            auth_provider=PlainTextAuthProvider(
                username=cassandra_settings.CASSANDRA_USER,
                password=cassandra_settings.CASSANDRA_PASSWORD
            )
        )
        
        # Устанавливаем соединение с кластером
        session = cluster.connect()
        
        # Создаем keyspace если он не существует
        # Keyspace - это пространство имен для таблиц в Cassandra
        session.execute(f"""
            CREATE KEYSPACE IF NOT EXISTS {cassandra_settings.CASSANDRA_KEYSPACE}
            WITH replication = {{'class': 'SimpleStrategy', 'replication_factor': 1}}
        """)
        
        # Выбираем keyspace для использования
        session.set_keyspace(cassandra_settings.CASSANDRA_KEYSPACE)
        
        # Инициализируем соединение для cqlengine
        # cqlengine - это ORM для работы с Cassandra
        connection.setup(
            [cassandra_settings.CASSANDRA_HOST],
            cassandra_settings.CASSANDRA_KEYSPACE,
            auth_provider=PlainTextAuthProvider(
                username=cassandra_settings.CASSANDRA_USER,
                password=cassandra_settings.CASSANDRA_PASSWORD
            ),
            port=cassandra_settings.CASSANDRA_PORT
        )
        
        # Синхронизируем модели с таблицами в базе данных
        # Это создаст таблицы, если они не существуют
        sync_table(Message)
        
        logger.info("Cassandra connection initialized successfully")
        return session
    except Exception as e:
        logger.error(f"Failed to initialize Cassandra connection: {str(e)}")
        raise 