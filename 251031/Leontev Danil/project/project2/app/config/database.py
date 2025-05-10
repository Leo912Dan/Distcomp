from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# =============================================
# Параметры подключения к базе данных
# =============================================

# ВАЖНО: Замените эти значения на те, которые вы указали при установке PostgreSQL
DB_USER = "postgres"  # Имя пользователя PostgreSQL
DB_PASSWORD = "postgres"  # Пароль, который вы задали при установке PostgreSQL
DB_HOST = "localhost"  # Хост, на котором запущен PostgreSQL
DB_PORT = "5432"  # Порт PostgreSQL
DB_NAME = "distcomp"  # Имя базы данных

# Создаем DSN строку для подключения
# DSN (Data Source Name) содержит все необходимые параметры для подключения
DSN = f"dbname={DB_NAME} user={DB_USER} password={DB_PASSWORD} host={DB_HOST} port={DB_PORT} client_encoding=utf8"

# =============================================
# Настройка SQLAlchemy
# =============================================

# Создаем движок базы данных
# pool_pre_ping=True - проверяет соединение перед использованием
# echo=True - выводит все SQL-запросы в консоль (полезно для отладки)
engine = create_engine(
    f"postgresql://",
    connect_args={"dsn": DSN},
    pool_pre_ping=True,
    echo=True
)

# Создаем фабрику сессий
# autocommit=False - изменения не сохраняются автоматически
# autoflush=False - изменения не отправляются в БД автоматически
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создаем базовый класс для моделей
# Все модели должны наследоваться от этого класса
Base = declarative_base()

def get_db():
    """
    Функция-генератор для получения сессии базы данных.
    Используется как зависимость в FastAPI.
    
    Yields:
        Session: Сессия базы данных
        
    Note:
        Сессия автоматически закрывается после использования
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 