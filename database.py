import os
from dotenv import load_dotenv
from sqlmodel import create_engine, SQLModel, Session

load_dotenv()  # take environment variables from .env.
SQLALCHEMY_DATABASE_URL = os.getenv('SQLALCHEMY_DATABASE_URL')
# SQLALCHEMY_DATABASE_URL = "postgresql://mlflow:mlflow_pass@postgres:5432/default"

# Create engine
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# Create table
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# Connet to database
def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()
