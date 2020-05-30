
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import db, setup_db, Movie, Actor


class CastingTestCase(unittest.TestCase):

    '''
    SETUP
    '''

    def setUp(self):
        '''define test variables and initialize app'''

        self.app = create_app()
        self.client = self.app.test_client
        setup_db(self.app)
        db.create_all()

        self.a_movie = {
            'title': 'FSDN - The Finale',
            'release_date': "2020-05-30"
        }

        self.an_invalid_movie = {
            'title': 'FSDN - The Failure',
            'release_dates': "2020-05-30"
        }

        self.an_updated_movie = {
            'title': 'FSDN - The Complete Failure',
            'release_dates': "2020-05-30"
        }

        self.an_actor = {
            'name': 'Hendrick H',
            'age': 25,
            'gender': 'Male',
            'movie_id': 1
        }

        self.an_invalid_actor = {
            'name': 'Hendrick H',
            'age': 35,
            'gender': 'Male',
            'movie_ids': 1
        }

        self.an_updated_actor = {
            'name': 'Hendrick Hendrick',
            'age': 25,
            'gender': 'Male',
            'movie_id': 1
        }

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        pass

    '''
    TEST CASES
    '''

    '''
    POST Endpoints
    '''

    def test_create_a_movie(self):
        response = self.client().post('/movies', json=self.a_movie)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_create_a_movie_fails_422_error(self):
        response = self.client().post('/movies', json=self.an_invalid_movie)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_create_an_actor(self):
        response = self.client().post('/actors', json=self.an_actor)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_create_an_actor_fails_422_error(self):
        response = self.client().post('/actors', json=self.an_invalid_actor)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)

    '''
    GET Endpoints
    '''

    def test_get_movies(self):

        response = self.client().get('/movies')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertNotEqual(len(data['movies']), 0)

    def test_get_actors(self):

        response = self.client().get('/actors')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertNotEqual(len(data['actors']), 0)

    '''
    PATCH Endpoints
    '''

    def test_update_a_movie(self):
        response = self.client().patch('/movies/1', json=self.an_updated_movie)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_update_a_movie_fails_404_error(self):
        response = self.client().patch('/movies/444', json=self.an_updated_movie)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_update_an_actor(self):
        response = self.client().patch('/actors/10', json=self.an_updated_actor)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_update_an_actor_fails_404_error(self):
        response = self.client().patch('/actors/444', json=self.an_updated_actor)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    '''
    DELETE Endpoints
    '''

    def test_delete_a_movie(self):

        # Create a new movie to be deleted later
        movie = Movie(title="FSDN - The Finale", release_date="2020-05-30")
        movie.insert()
        movie_id = movie.id

        response = self.client().delete('/movies/{}'.format(movie_id))
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], "Movie record deletion completed")
        self.assertEqual(data['deleted'], movie_id)

    def test_delete_a_movie_fails_404_error(self):

        response = self.client().delete('/movies/444')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_delete_an_actor(self):

        # Create a new actor to be deleted later
        actor = Actor(name="Hemilly", age="240", gender="Male", movie_id=1)
        actor.insert()
        actor_id = actor.id

        response = self.client().delete('/actors/{}'.format(actor_id))
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], "Actor record deletion completed")
        self.assertEqual(data['deleted'], actor_id)

    def test_delete_an_actor_fails_404_error(self):

        response = self.client().delete('/actors/444')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)


if __name__ == "__main__":
    unittest.main()
