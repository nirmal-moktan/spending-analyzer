import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL


# Locating and load the .env file
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path)

# Build the PostgreSQL connection URL
database_url = URL.create(
    drivername="postgresql+psycopg",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT", "5432")),
    database=os.getenv("DB_NAME"),
)

# Create the SQLAlchemy engine
engine = create_engine(database_url)


def main():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT current_database()"))
        print("Connected to:", result.scalar_one())

if __name__ == "__main__":
    main()