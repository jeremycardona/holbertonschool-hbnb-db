# src/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from dotenv import load_dotenv
import os
from src.models.base import Base
load_dotenv()

# Determine the database URL based on environment variables
if os.getenv('DATABASE_TYPE') == 'sqlite':
    database_url = os.getenv('DATABASE_URL')
elif os.getenv('DATABASE_TYPE') == 'postgresql':
    database_url = os.getenv('DATABASE_URL')
else:
    raise ValueError('Unsupported DATABASE_TYPE. Use "sqlite" or "postgresql".')

engine = create_engine(database_url)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

def init_db():
    import src.models  # Import all your models here
    Base.metadata.create_all(bind=engine)
