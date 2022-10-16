"""
Module for database related stuff to keep the main.py clean
"""

from os import environ  # pylint: disable=unused-import   #for dev env
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# SQLALCHEMY_DATABASE_URL =
# "postgresql://<username>:<password>@<ip-address/hostname>/<database_name>"
SQLALCHEMY_DATABASE_URL = environ.get("DB_CONNECTION_STRING")

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    """
    Initialize connection to the database on every API request
    """
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()
