# app.py

from flask import Flask, request
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['RESTX_JSON'] = {'ensure_ascii': False, 'indent': 2}

db = SQLAlchemy(app)


class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    trailer = db.Column(db.String(255))
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"))
    genre = db.relationship("Genre")
    director_id = db.Column(db.Integer, db.ForeignKey("director.id"))
    director = db.relationship("Director")


class MovieSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str()
    description = fields.Str()
    trailer = fields.Str()
    year = fields.Int()
    rating = fields.Float()
    genre_id = fields.Int()
    genre = fields.Str()
    director_id = fields.Int()
    director = fields.Str()


movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)


class Director(db.Model):
    __tablename__ = 'director'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class DirectorSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()


director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)


class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class GenreSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()


genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)

api = Api(app)
movie_ns = api.namespace('movies')


@movie_ns.route('/')
class MoviesView(Resource):
    def get(self):
        director_req = request.args.get('director_id')
        genre_req = request.args.get('genre_id')

        """return movie by director"""
        if director_req is not None:
            movies = Movie.query.filter(Movie.director_id == director_req).all()
            return movies_schema.dump(movies), 200

            """return movies by genre"""
        elif genre_req is not None:
            movies = Movie.query.filter(Movie.genre_id == genre_req).all()
            return movies_schema.dump(movies), 200

        """return all movies"""
        all_movies = Movie.query.all()
        return movies_schema.dump(all_movies), 200


@movie_ns.route('/<int:mid>')
class MovieView(Resource):
    def get(self, mid: int):
        """return movie_by_id"""
        movie = Movie.query.get(mid)
        return movie_schema.dump(movie), 200


if __name__ == '__main__':
    app.run(debug=True)
