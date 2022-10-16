"""
Main file to run the API
"""

from fastapi import FastAPI
from .routers import recipies


app = FastAPI()

app.include_router(recipies.router)


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
