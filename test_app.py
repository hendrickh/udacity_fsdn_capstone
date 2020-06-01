import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import db, setup_db, Movie, Actor

'''
AUTH SETUP
Roles:
Casting Assistant - VIEW ONLY
Casting Director - VIEW + ADD/DELETE ACTORS + PATCH ACTORS/MOVIES
Executive Producer - ALL
'''

casting_assistant_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InVhU"\
    "k9nbjc4U1ZSSzhzZE8zcEd4NCJ9.eyJpc3MiOiJodHRwczovL"\
    "2hlbmRoLWZzbmQuZXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dG"\
    "gwfDVlZDJlNTk4NzMwODMwMGMxZWEyMzViMSIsImF1ZCI6IkN"\
    "hc3RpbmciLCJpYXQiOjE1OTEwMDI1NTgsImV4cCI6MTU5MTA4"\
    "ODk1OCwiYXpwIjoiUjlEQTdjWE0xbmZmcUdtRHdyWG40VjN4e"\
    "mdvN2Ryc0wiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbIm"\
    "dldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.LxpY0BlW_Zo7xQ"\
    "qWrOp3hQ5_AebZS0zwrmzUJKYh9LhLSBAjfCmEep6m-F1aTOI"\
    "WRSkS6_ZnHpIF7yfWeXPQcpOgtSlwSwqtGpZTaJDoCijrED8k"\
    "Hw3EvkmJfn7GWQ9GnDMRMZbKA5zp2lVmfD7hcrJr1tnAomLVX"\
    "q1Fbtc5av1vHan5C4CL5ZahSxRuYssl9oo1S4jCo9eH860tfX"\
    "2eNJqAm_t5yWXDqhxVeG9XdWUUzxDStcw01dco-8o-60Bjd_D"\
    "RZkArR8dwzB-UVs-G5d3FnBpimrfMfg98tjwCUwukOurzFsY4"\
    "JXj5IT-n4kX8fRfxEGbHLL2JOTRbdFVXKQ"
casting_director_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InVhU"\
    "k9nbjc4U1ZSSzhzZE8zcEd4NCJ9.eyJpc3MiOiJodHRwczovL"\
    "2hlbmRoLWZzbmQuZXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dG"\
    "gwfDVlZDJlNWJkMjE3NjE4MGMwY2ZjYWEyNyIsImF1ZCI6IkN"\
    "hc3RpbmciLCJpYXQiOjE1OTEwMDI2MzYsImV4cCI6MTU5MTA4"\
    "OTAzNiwiYXpwIjoiUjlEQTdjWE0xbmZmcUdtRHdyWG40VjN4e"\
    "mdvN2Ryc0wiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbIm"\
    "RlbGV0ZTphY3RvcnMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdml"\
    "lcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBv"\
    "c3Q6YWN0b3JzIl19.m9Ib169YxWA4hNZKXTfXa16_9RLpoo4l"\
    "_rSEQEGIn2TItRFc8GOIJ9WZSfjhiwOn9j9O6KSKBHDp9nNSt"\
    "_b4FlIppvAQ4NH01MDh8NaQzPECxtwfDBPFd0MUKUxD_IEiTx"\
    "GslrtA16W1dQ1nsImjDUb6nK1LMnEcsayGCOTWBgzS_a7kspP"\
    "-5-tbn-YBYJRtfwOd2bcUOD7skCkrhEqU6JdqIppN9WeCBY7K"\
    "AlGMZth3pffb7Es5KMvsSxW60Vnm67EBiwqt15Y_Zu9cqYnO9"\
    "Xi3VoGg4l_QxiEm6z29LmHukakR3nIKrF5qX8oWrXTq33SThI"\
    "05e8hjeJMk4qm_3A"
executive_producer_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InVhU"\
    "k9nbjc4U1ZSSzhzZE8zcEd4NCJ9.eyJpc3MiOiJodHRwczovL"\
    "2hlbmRoLWZzbmQuZXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dG"\
    "gwfDVlZDJlNWRjOGM5YjAwMGMwOGJmY2I1MiIsImF1ZCI6IkN"\
    "hc3RpbmciLCJpYXQiOjE1OTEwMDI2ODksImV4cCI6MTU5MTA4"\
    "OTA4OSwiYXpwIjoiUjlEQTdjWE0xbmZmcUdtRHdyWG40VjN4e"\
    "mdvN2Ryc0wiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbIm"\
    "RlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmF"\
    "jdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJw"\
    "YXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92a"\
    "WVzIl19.yB-s9WfseI6Rf-Kuib6aDfSnkUFETb0b0w3zrBez0"\
    "IVo5_stHVnpiikjarKOLftOZwjsR5VdXJq8NEbVbpgcWi8gkm"\
    "psLHXR24TSP3muODG5WpQGqIq4WcpuQdrhSzDqLR41fpKN4gJ"\
    "x-hBfrIEkDdfpqlWjPBae-7EJkfJ13yug2bG0TAW-7KlxnlfH"\
    "MIQwS9VUGuU24zBYYG4JEqXae8TmcGqHDZr0hzPJZn_TvD3cO"\
    "9HSuxgs1WBV3Lz0LcKx_VfwHnmVKq04aPuCz8C6ZsQbI12IPD"\
    "qvYfFz1ur4N4HZ-1XwixtDRZsj05v3QZYb1H-rzA8ax7UfNfx"\
    "9aqZbng"

casting_assistant_auth_header = {
    'Authorization': "Bearer " + casting_assistant_token
}

casting_director_auth_header = {
    'Authorization': "Bearer " + casting_director_token
}

executive_producer_auth_header = {
    'Authorization': "Bearer " + executive_producer_token
}


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
        response = self.client().post('/movies', json=self.a_movie,
                                      headers=executive_producer_auth_header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_create_a_movie_fails_422_error(self):
        response = self.client().post('/movies', json=self.an_invalid_movie,
                                      headers=executive_producer_auth_header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_create_a_movie_fails_401_error(self):
        response = self.client().post('/movies', json=self.a_movie,
                                      headers=casting_director_auth_header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_create_an_actor(self):
        response = self.client().post('/actors', json=self.an_actor,
                                      headers=casting_director_auth_header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_create_an_actor_fails_422_error(self):
        response = self.client().post('/actors', json=self.an_invalid_actor,
                                      headers=casting_director_auth_header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_create_an_actor_fails_401_error(self):
        response = self.client().post('/actors', json=self.an_invalid_actor,
                                      headers=casting_assistant_auth_header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)

    '''
    GET Endpoints
    '''

    def test_get_movies(self):

        response = self.client().get('/movies',
                                     headers=casting_assistant_auth_header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertNotEqual(len(data['movies']), 0)

    def test_get_movies_fails_401_error(self):

        response = self.client().get('/movies')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_get_actors(self):

        response = self.client().get('/actors',
                                     headers=casting_assistant_auth_header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertNotEqual(len(data['actors']), 0)

    def test_get_actors_fails_401_error(self):

        response = self.client().get('/actors')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)

    '''
    PATCH Endpoints
    '''

    def test_update_a_movie(self):
        response = self.client().patch('/movies/1',
                                       json=self.an_updated_movie,
                                       headers=casting_director_auth_header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_update_a_movie_fails_404_error(self):
        response = self.client().patch('/movies/444',
                                       json=self.an_updated_movie,
                                       headers=casting_director_auth_header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_update_a_movie_fails_401_error(self):
        response = self.client().patch('/movies/444',
                                       json=self.an_updated_movie,
                                       headers=casting_assistant_auth_header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_update_an_actor(self):
        response = self.client().patch('/actors/1',
                                       json=self.an_updated_actor,
                                       headers=casting_director_auth_header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_update_an_actor_fails_404_error(self):
        response = self.client().patch('/actors/444',
                                       json=self.an_updated_actor,
                                       headers=casting_director_auth_header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_update_an_actor_fails_401_error(self):
        response = self.client().patch('/actors/444',
                                       json=self.an_updated_actor,
                                       headers=casting_assistant_auth_header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)

    '''
    DELETE Endpoints
    '''

    def test_delete_a_movie(self):

        # Create a new movie to be deleted later
        movie = Movie(title="FSDN - The Finale", release_date="2020-05-30")
        movie.insert()
        movie_id = movie.id

        response = self.client().delete('/movies/{}'.format(movie_id),
                                        headers=executive_producer_auth_header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], "Movie record deletion completed")
        self.assertEqual(data['deleted'], movie_id)

    def test_delete_a_movie_fails_404_error(self):

        response = self.client().delete(
            '/movies/444', headers=executive_producer_auth_header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_delete_a_movie_fails_401_error(self):

        response = self.client().delete('/movies/444',
                                        headers=casting_director_auth_header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_delete_an_actor(self):

        # Create a new actor to be deleted later
        actor = Actor(name="Hemilly", age="240", gender="Male", movie_id=1)
        actor.insert()
        actor_id = actor.id

        response = self.client().delete('/actors/{}'.format(actor_id),
                                        headers=casting_director_auth_header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], "Actor record deletion completed")
        self.assertEqual(data['deleted'], actor_id)

    def test_delete_an_actor_fails_404_error(self):

        response = self.client().delete('/actors/444',
                                        headers=casting_director_auth_header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_delete_an_actor_fails_401_error(self):

        response = self.client().delete('/actors/444',
                                        headers=casting_assistant_auth_header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)


if __name__ == "__main__":
    unittest.main()
