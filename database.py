import os
from dotenv import load_dotenv
from sqlmodel import create_engine, SQLModel, Session

load_dotenv()  # take environment variables from .env.
# SQLALCHEMY_DATABASE_URL = os.getenv('SQLALCHEMY_DATABASE_URL')

# Set the SQLAlchemy database URL based on your MySQL configuration
SQLALCHEMY_DATABASE_URL = f"mysql+mysqlconnector://trainUser:password@localhost:3306/traindatabase"

# Print the database URL for debugging (optional)
print(SQLALCHEMY_DATABASE_URL)

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
