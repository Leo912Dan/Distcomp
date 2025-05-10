# Discussion Service

Микросервис для управления сообщениями в системе обсуждений.

## Описание

Этот микросервис отвечает за хранение и управление сообщениями в системе. Он использует Cassandra в качестве базы данных для обеспечения высокой производительности и масштабируемости.

## Требования

- Python 3.11+
- Docker и Docker Compose
- Cassandra 4.1+

## Установка и запуск

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd discussion-service
```

2. Запустите сервис с помощью Docker Compose:
```bash
docker-compose up --build
```

Сервис будет доступен по адресу: http://localhost:24112

## API Endpoints

- `POST /api/v1.0/messages/` - Создание нового сообщения
- `GET /api/v1.0/messages/{message_id}` - Получение сообщения по ID
- `GET /api/v1.0/messages/topic/{topic_id}` - Получение всех сообщений топика
- `PUT /api/v1.0/messages/{message_id}` - Обновление сообщения
- `DELETE /api/v1.0/messages/{message_id}` - Удаление сообщения
- `GET /health` - Проверка здоровья сервиса

## Конфигурация

Сервис настраивается через переменные окружения:

- `CASSANDRA_HOSTS` - Список хостов Cassandra
- `CASSANDRA_PORT` - Порт Cassandra
- `CASSANDRA_KEYSPACE` - Имя keyspace
- `CASSANDRA_USERNAME` - Имя пользователя
- `CASSANDRA_PASSWORD` - Пароль

## Разработка

1. Установите зависимости:
```bash
pip install -r requirements.txt
```

2. Запустите тесты:
```bash
pytest
```

## Лицензия

MIT 