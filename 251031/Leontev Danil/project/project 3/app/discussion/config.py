from pydantic_settings import BaseSettings

class CassandraSettings(BaseSettings):
    CASSANDRA_HOSTS: list[str] = ["localhost"]
    CASSANDRA_PORT: int = 9042
    CASSANDRA_KEYSPACE: str = "discussion"
    CASSANDRA_USERNAME: str = "cassandra"
    CASSANDRA_PASSWORD: str = "cassandra"

    class Config:
        env_prefix = "CASSANDRA_"

cassandra_settings = CassandraSettings() 