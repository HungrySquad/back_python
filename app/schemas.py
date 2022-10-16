# pylint: disable=no-name-in-module
# pylint: disable=too-few-public-methods
"""
Module to store validation chemas constructed using pydantic
used by api to validate and select/format
the in
coming and outgoing requests
"""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class RecipyBase(BaseModel):
    """
    Base for Schemas
    """

    name: str
    url: Optional[str] = None
    img_url: Optional[str] = None
    time_values: list
    servings: str
    description: str
    ingredients: list
    nutritions: Optional[list] = None
    instructions: str


class RecipyCreate(RecipyBase):
    """
    RecipyCreate Schema that can be extended
    """


class RecipyResponse(RecipyBase):
    """
    RecipyResponse Schema to format outgoing requests
    """

    id: int
    posted_at: datetime

    class Config:
        """
        Configuration for the previous class to use the orm_mode
        """

        orm_mode = True
