# pylint: disable=too-few-public-methods
"""
Module to store the models for the sqlalchemy to work with database
"""
from sqlalchemy import TIMESTAMP, Column, Integer, String, ARRAY, text
from .database import Base


class Recipy(Base):
    """
    Base Recipy table model that will be interacted with by API
    """

    __tablename__ = "recipies"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    url = Column(String, nullable=True, default=None)
    img_url = Column(String, nullable=True, default=None)
    time_values = Column(ARRAY(String), nullable=True, default=None)
    servings = Column(String, nullable=False, default=None)
    description = Column(String, nullable=False)
    ingredients = Column(ARRAY(String), nullable=False)
    nutritions = Column(ARRAY(String), nullable=True, default=None)
    instructions = Column(String, nullable=True)
    posted_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text('now()')
    )
