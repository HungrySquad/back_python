"""
Testing Version of the API using Flask/SQLAlchemy/Marshmallow
"""

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy  # new
from flask_marshmallow import Marshmallow  # new
from flask_restful import Api, Resource  # new
from marshmallow import Schema, fields, post_load, ValidationError
from waitress import serve

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///recipies.db"  # use sqlite for now

db = SQLAlchemy(app)  # new light one-file db

ma = Marshmallow(app)  # new scheme documentation

api = Api(app)  # new restful api for flask

"Diasbled too-few-public-methods due to the class Post needing to be this way to be corretly Mapped"


class Post(db.Model):  # pylint: disable=too-few-public-methods
    """
    Class Post for creating a db.Model for new entries in the SQLALCHEMY database
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    ingredients = db.Column(db.String(255))
    image = db.Column(db.String(255), nullable=True)
    time = db.Column(db.String(255))
    description = db.Column(db.String(3000))
    source = db.Column(db.String(255))
    nutrients = db.Column(db.String(255))
    instructions = db.Column(db.String(4000))
    servings = db.Column(db.String(255))

    def __repr__(self):
        return f"<Recipy {self.name}>"


class PostSchema(Schema):
    """
    Schema for serializing and de-serializing the data
    """

    # class Meta:
    #     fields = ("id", "name", "ingredients","nutrients", "description","time", "source")
    #     model = Post
    name = fields.Str()
    id = fields.Int()
    ingredients = fields.Str()
    nutrients = fields.Str()
    description = fields.Str()
    time = fields.Str()
    source = fields.Str()
    image = fields.Str()
    servings = fields.Str(required=True, default="1")
    instructions = fields.Str()

    @post_load
    def create_post(self, data, **kwargs):  # pylint: disable=unused-argument
        """
        Method to validate the data using the Scheme and return the data in db object
        """
        new_post = Post(
            name=data["name"],
            ingredients=data["ingredients"],
            time=data["time"],
            source=data["source"],
            nutrients=data["nutrients"],
            description=data["description"],
            image=data["image"],
            instructions=data["instructions"],
            servings=data["servings"]
        )
        return new_post


class PostListResource(Resource):
    """
    Class for the REST flask api which describes 2
    REST methods Used for  get (all entries) and single post
    """

    def get(self):
        """
        REST API 'GET' method to retrieve all API entries
        """
        posts = Post.query.all()
        return posts_schema.dump(posts)

    def post(self):
        """
        REST API 'POST' method to add a new API entry
        """
        try:
            db_post_data = post_schema.load(request.json)
            db.session.add(db_post_data)
            db.session.commit()
            return {f"{str(db_post_data)} has been added": True}
        except ValidationError as error:
            return str(error)


class PostResource(Resource):
    """
    Class for the REST flask api which describes 3
    REST methods used for get(single) and patch/delte (single)
    """

    def get(self, post_id):
        """
        REST API 'GET' method to retrieve single API entry by post_id
        """
        post = Post.query.get_or_404(post_id)
        return post_schema.dump(post)

    def patch(self, post_id):
        """
        REST API 'PATCH' method to patch an API entry by post_id
        """
        post = Post.query.get_or_404(post_id)  # object of the POST class by ID
        post.query.update(request.json)
        # request.json
        # {
        # 'name': 'Chocolate',
        # 'ingredients': 'Lorem ipsum',
        # 'cookTime': 'Lorem Ipsum 5 m',
        # 'prepTime': 'LoremIpsum 10m',
        # 'source': 'your mom'
        # }

        db.session.commit()
        return post_schema.dump(post)

    def delete(self, post_id):
        """
        REST API 'DELETE' method to delete an API entry by post_id
        """
        post = Post.query.get_or_404(post_id)
        db.session.delete(post)
        db.session.commit()
        return "", 204


api.add_resource(PostResource, "/posts/<int:post_id>")

db.create_all()

post_schema = PostSchema()
posts_schema = PostSchema(many=True)
api.add_resource(PostListResource, "/posts")


if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8080)
