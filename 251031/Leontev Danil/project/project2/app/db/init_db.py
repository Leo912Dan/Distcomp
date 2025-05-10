from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from app.config.database import Base, engine
from app.models.entities import User, Topic, Mark, Message

def init_db():
    """
    Инициализирует базу данных.
    Создает все необходимые таблицы в базе данных PostgreSQL.
    
    Создаваемые таблицы:
    - tbl_user: таблица пользователей
    - tbl_topic: таблица тем обсуждений
    - tbl_mark: таблица меток
    - tbl_message: таблица сообщений
    - tbl_topic_mark: связующая таблица для связи многие-ко-многим между темами и метками
    
    Raises:
        OperationalError: Если не удалось подключиться к базе данных
    """
    try:
        # Создаем все таблицы
        Base.metadata.create_all(bind=engine)
        print("База данных успешно инициализирована!")
        print("Созданы таблицы:")
        print("- tbl_user")
        print("- tbl_topic")
        print("- tbl_mark")
        print("- tbl_message")
        print("- tbl_topic_mark")
    except OperationalError as e:
        print("Ошибка подключения к базе данных:")
        print("1. Убедитесь, что PostgreSQL установлен и запущен")
        print("2. Проверьте, что база данных 'distcomp' существует")
        print("3. Проверьте параметры подключения:")
        print("   - Хост: localhost")
        print("   - Порт: 5432")
        print("   - Пользователь: postgres")
        print("   - Пароль: postgres")
        print("\nПодробная ошибка:", str(e))

if __name__ == "__main__":
    # Если файл запущен напрямую, инициализируем базу данных
    init_db() 