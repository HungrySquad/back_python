from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy  # new
from flask_marshmallow import Marshmallow  # new
from flask_restful import Api, Resource  # new
from marshmallow import Schema, fields, post_load, ValidationError

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///recipies.db"  # use sqlite for now

db = SQLAlchemy(app)  # new light one-file db

ma = Marshmallow(app)  # new scheme documentation

api = Api(app)  # new restful api for flask


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    ingredients = db.Column(db.String(255))
    image = db.Column(db.String(255), nullable=True)
    time = db.Column(db.String(255))
    description= db.Column(db.String(255))
    source = db.Column(db.String(255))
    nutrients = db.Column(db.String(255))
    def __repr__(self):
        return "<Recipy %s>" % self.name


class PostSchema(Schema):
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
    servings = fields.Str(required=False,default="")

    @post_load
    def create_post(self,data,**kwargs):
        new_post = Post(
            # id=data['id'],
            name=data["name"],
            ingredients=data["ingredients"],
            time=data["time"],
            source=data["source"],
            nutrients=data["nutrients"],
            description=data["description"],
            image=data['image']
        )
        return new_post

class PostListResource(Resource):
    def get(self):
        posts = Post.query.all()
        return posts_schema.dump(posts)

    def post(self):
        
        try: 
            db_post_data = post_schema.load(request.json)
            db.session.add(db_post_data)
            db.session.commit()
            return {f"{str(db_post_data)} has been added":True}
        except ValidationError as e:
            return str(e)

class PostResource(Resource):
    def get(self, post_id):
        post = Post.query.get_or_404(post_id)
        return post_schema.dump(post)

    def patch(self, post_id):
        post = Post.query.get_or_404(post_id)  # object of the POST class by ID
        post.query.update(request.json)
        # request.json  {'name': 'Chocolate', 'ingredients': 'Lorem ipsum', 'cookTime': 'Lorem Ipsum 5 m', 'prepTime': 'LoremIpsum 10m', 'source': 'your mom'}

        db.session.commit()
        return post_schema.dump(post)

    def delete(self, post_id):
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
    app.run(debug=True)
