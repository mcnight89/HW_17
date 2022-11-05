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
director_ns = api.namespace('director')
genre_ns = api.namespace('genres')


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

    def post(self):
        req_json = request.json
        new_movie = Movie(**req_json)
        with db.session.begin():
            db.session.add(new_movie)
        return "", 201


@movie_ns.route('/<int:mid>')
class MovieView(Resource):
    def get(self, mid: int):
        """return movie_by_id"""
        movie = Movie.query.get(mid)
        return movie_schema.dump(movie), 200

    def put(self, mid: int):
        movie = Movie.query.get(mid)
        req_json = request.json

        movie.id = req_json.get("id")
        movie.title = req_json.get("title")
        movie.description = req_json.get("description")
        movie.trailer = req_json.get("trailer")
        movie.year = req_json.get("year")
        movie.rating = req_json.get("rating")
        movie.genre_id = req_json.get("genre_id")
        movie.genre = req_json.get("genre")
        movie.director_id = req_json.get("director_id")
        movie.director = req_json.get("director")

        db.session.add(movie)
        db.session.commit()
        return "", 204

    def delete(self, mid: int):
        movie = Movie.query.get(mid)
        db.session.delete(movie)
        db.session.commit()
        return "", 204


@director_ns.route('/<int:mid>')
class DirectorView(Resource):

    def post(self):
        req_json = request.json
        new_director = Director(**req_json)
        with db.session.begin():
            db.session.add(new_director)
        return "", 201

    def put(self, mid: int):
        director = Director.query.get(mid)
        req_json = request.json

        director.id = req_json.get("id")
        director.name = req_json.get("name")

        db.session.add(director)
        db.session.commit()
        return "", 204

    def delete(self, mid: int):
        director = Director.query.get(mid)
        db.session.delete(director)
        db.session.commit()
        return "", 204


@genre_ns.route('/<int:mid>')
class GenreView(Resource):

    def post(self):
        req_json = request.json
        new_genre = Genre(**req_json)
        with db.session.begin():
            db.session.add(new_genre)
        return "", 201

    def put(self, mid: int):
        genre = Genre.query.get(mid)
        req_json = request.json

        genre.id = req_json.get("id")
        genre.name = req_json.get("name")

        db.session.add(genre)
        db.session.commit()
        return "", 204

    def delete(self, mid: int):
        genre = Genre.query.get(mid)
        db.session.delete(genre)
        db.session.commit()
        return "", 204


if __name__ == '__main__':
    app.run(debug=True)
