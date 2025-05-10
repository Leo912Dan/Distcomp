from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from .config import cassandra_settings
import time

def init_cassandra():
    # Подключаемся к Cassandra
    auth_provider = PlainTextAuthProvider(
        username=cassandra_settings.CASSANDRA_USERNAME,
        password=cassandra_settings.CASSANDRA_PASSWORD
    )
    
    cluster = Cluster(
        contact_points=cassandra_settings.CASSANDRA_HOSTS,
        port=cassandra_settings.CASSANDRA_PORT,
        auth_provider=auth_provider
    )
    
    session = cluster.connect()
    
    # Создаем keyspace
    session.execute(f"""
        CREATE KEYSPACE IF NOT EXISTS {cassandra_settings.CASSANDRA_KEYSPACE}
        WITH replication = {{'class': 'SimpleStrategy', 'replication_factor': 1}}
    """)
    
    # Используем keyspace
    session.set_keyspace(cassandra_settings.CASSANDRA_KEYSPACE)
    
    # Создаем таблицу messages
    session.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id uuid PRIMARY KEY,
            content text,
            topic_id uuid,
            user_id uuid,
            created_at timestamp,
            updated_at timestamp
        )
    """)
    
    # Создаем индексы
    session.execute("""
        CREATE INDEX IF NOT EXISTS ON messages (topic_id)
    """)
    session.execute("""
        CREATE INDEX IF NOT EXISTS ON messages (user_id)
    """)
    
    session.shutdown()
    cluster.shutdown()

def wait_for_cassandra():
    max_retries = 30
    retry_interval = 2
    
    for i in range(max_retries):
        try:
            init_cassandra()
            print("Successfully connected to Cassandra")
            return
        except Exception as e:
            print(f"Failed to connect to Cassandra (attempt {i+1}/{max_retries}): {str(e)}")
            if i < max_retries - 1:
                time.sleep(retry_interval)
            else:
                raise Exception("Failed to connect to Cassandra after maximum retries") 