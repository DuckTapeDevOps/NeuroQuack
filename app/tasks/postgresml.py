import os
from sqlalchemy import create_engine, text
from pydantic import BaseModel, PostgresDsn


POSTGRESML_PASSWORD = os.environ.get("POSTGRESQL_PASSWORD", "password-not-set")

class DatabaseConfig(BaseModel):
    username: str
    password: str
    host: str = "localhost"
    port: str = "5433"
    database: str = "postgresml"
    db_url: PostgresDsn = None

    class Config:
        env_prefix = 'DB_'  # prefixes for environment variables

    @property
    def sqlalchemy_database_url(self) -> str:
        return f"postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"

# Example usage
config = DatabaseConfig(username="NeuroQuack", password=POSTGRESML_PASSWORD)
db_string = config.sqlalchemy_database_url

# print(db_string)
