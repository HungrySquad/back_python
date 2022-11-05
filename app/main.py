"""
Main file to run the API
"""

from fastapi import FastAPI
from .routers import recipies
from fastapi_pagination import add_pagination

app = FastAPI()

app.include_router(add_pagination(recipies.router))


# id: ". . ."
# name: ". . ."
# url: ". . ."
# img_url: ". . ."
# time_values: {. . .}
# servings: ". . ."
# description: ". . ."
# ingredients: ". . ."
# nutirtions: {. . .}
# instructions ". . ."
