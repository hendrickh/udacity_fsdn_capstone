import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Movie, Actor, db
from auth import AuthError, requires_auth


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={'/': {'origins': '*'}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, PUT, POST, DELETE, OPTIONS')
        return response

    '''
    GET Endpoints
    '''

    @app.route('/movies')
#    @requires_auth('view:movies')
    def get_movies():
        movies = Movie.query.all()
        movies = [movie.format() for movie in movies]
        for movie in movies:
            movie['actors'] = [actor.format() for actor in movie['actors']]

        return jsonify({
            'success': True,
            'movies': movies
        }), 200

    @app.route('/actors')
#    @requires_auth('view:actors')
    def get_actors():
        actors = Actor.query.all()

        return jsonify({
            'success': True,
            'actors': [actor.format() for actor in actors]
        }), 200

    '''
    DELETE Endpoints
    '''

    @app.route('/movies/<int:id>', methods=['DELETE'])
#    @requires_auth('delete:movie')
    def delete_movie(id):
        try:
            movie = Movie.query.filter_by(id=id).one_or_none()
            print("OMG WHY")
            if not movie:
                abort(404)

            movie.delete()

            return jsonify({
                "success": True,
                "message": "Movie record deletion occured",
                'deleted': id
            })

        except:
            abort(422)

    @app.route('/actors/<int:id>', methods=['DELETE'])
#    @requires_auth('delete:actor')
    def delete_actor(id):
        try:
            actor = Actor.query.filter_by(id=id).one_or_none()

            if not actor:
                abort(404)

            actor.delete()

            return jsonify({
                "success": True,
                "message": "Actor record deletion occured",
                'deleted': id
            })

        except:
            abort(422)

    '''
    POST Endpoints
    '''

    @app.route('/movies', methods=['POST'])
#    @requires_auth('post:movie')
    def post_new_movie():

        body = request.get_json()

        if ((body.get('title') is None) or (body.get('release_date') is None)):
            abort(422)

        else:
            new_title = body.get('title')
            new_release_date = body.get('release_date')

            try:
                movie = Movie(
                    title=new_title,
                    release_date=new_release_date
                )

                movie.insert()

                new_movie = Movie.query.get(movie.id)

                return jsonify({
                    'success': True,
                    'created': movie.id,
                    'new_movie': new_movie.format()
                })

            except:
                abort(422)

    @app.route('/actors', methods=['POST'])
#    @requires_auth('post:actor')
    def post_new_actor():
        body = request.get_json()#

        # In this validation, the actor's 'movie_id' has been ignored to account for budding actors who have yet to start acting in any movies.

        if ((body.get('name') is None) or (body.get('age') is None) or (body.get('gender') is None)):
            abort(422)

        else:
            new_name = body.get('name')
            new_age = body.get('age')
            new_gender = body.get('gender')
            new_movie_id = body.get('movie_id', None)

            try:
                actor = Actor(
                    name=new_name,
                    age=new_age,
                    gender=new_gender,
                    movie_id=new_movie_id
                )

                actor.insert()

                new_actor = Actor.query.get(actor.id)

                return jsonify({
                    'success': True,
                    'created': actor.id,
                    'new_movie': new_actor.format()
                })

            except:
                abort(422)

    '''
    PATCH Endpoints
    '''

    @app.route('/movies/<int:id>', methods=['PATCH'])
#    @requires_auth('patch:movies')
    def patch_movie(id):
        body = request.get_json()

        movie = Movie.query.filter(Movie.id == id).one_or_none()

        if not movie:
            abort(404)

        try:
            title = body.get('title')
            release_date = body.get('release_date')

            if title:
                movie.title = title

            if release_date:
                movie.release_date = release_date

            movie.update()

            return jsonify({
                "success": True,
                "message": "Movie record update completed"
            })

        except:
            abort(422)

    @app.route('/actors/<int:id>', methods=['PATCH'])
#    @requires_auth('patch:actors')
    def patch_actor(id):
        body = request.get_json()

        actor = Actor.query.filter(Actor.id == id).one_or_none()

        if not actor:
            abort(404)

        try:
            name = body.get('name')
            age = body.get('age')
            gender = body.get('gender')
            movie_id = body.get('movie_id')

            if name:
                actor.name = name

            if age:
                actor.age = age

            if gender:
                actor.gender = gender

            if movie_id:
                actor.movie_id = movie_id

            actor.update()

            return jsonify({
                "success": True,
                "message": "Actor record update completed"
            })

        except:
            abort(422)

    '''
    Error Handlers
    '''

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'resource not found'
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable'
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'bad request'
        }), 400

    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error['description']
        }), error.status_code

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
