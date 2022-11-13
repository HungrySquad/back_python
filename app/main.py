"""
Main file to run the API
"""

from fastapi import FastAPI
from fastapi_pagination import add_pagination
from starlette.middleware.cors import CORSMiddleware

from .routers import recipies

app = FastAPI()

app.include_router(add_pagination(recipies.router))

app.add_middleware(
CORSMiddleware,
allow_origins=["*"], # Allows all origins
allow_credentials=True,
allow_methods=["*"], # Allows all methods
allow_headers=["*"], # Allows all headers
)
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
