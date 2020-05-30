
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

bearer_tokens = {
    "casting_assistant" : "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InVhUk9nbjc4U1ZSSzhzZE8zcEd4NCJ9.eyJpc3MiOiJodHRwczovL2hlbmRoLWZzbmQuZXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlZDJlNTk4NzMwODMwMGMxZWEyMzViMSIsImF1ZCI6IkNhc3RpbmciLCJpYXQiOjE1OTA4ODAyMzQsImV4cCI6MTU5MDk2NjYzNCwiYXpwIjoiUjlEQTdjWE0xbmZmcUdtRHdyWG40VjN4emdvN2Ryc0wiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.SKwJC_6SOmh09u-FTbAaW18TG09RjNmwne7BB3FAtSX9ll7QEneWJ65y156c1uoK1FZHpN3UXLV0ZTypP_cCoLCIUyl0wbMlY0R2s3wMIfZzdmg7ezdW1lgtDSME0-2ey7LdQH0hl0w-CEPwQiWIdg_P5tC5Gqi693WwbD59CUdvaMkMEzbS8yGDRQzWGUhmXq7HSgU3i-L0p-6eTAg_SUnWnt2iHwukorET9D_LoaLiIkGZTud3nZcakQveet09IOOKejQoHWyr9-3CHhvSY7JBfu_e66zbBt4ftA1WvTT3nhTlNv_4Y3WVddYMMz5fQkhZayme0QPfVK5UUKeCIw",
    "casting_director" : "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InVhUk9nbjc4U1ZSSzhzZE8zcEd4NCJ9.eyJpc3MiOiJodHRwczovL2hlbmRoLWZzbmQuZXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlZDJlNWJkMjE3NjE4MGMwY2ZjYWEyNyIsImF1ZCI6IkNhc3RpbmciLCJpYXQiOjE1OTA4ODAzMDgsImV4cCI6MTU5MDk2NjcwOCwiYXpwIjoiUjlEQTdjWE0xbmZmcUdtRHdyWG40VjN4emdvN2Ryc0wiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIl19.Jta99zCY-kj_B_mdCWeGNMQ05cgyvFTFSdyctp1_F-oZTujHXcQZkUsPQfUxJPZ_Z8VPgmJc3WDiUhLPgWnYzrACRoHuRyA7knv7ZQgRwNl5awH1F6fXwcvJowSDCVjiXbzAu97D021tLP57gvMARPubh73GhNkVJr-7jif2IT4T3EAbjzCmJbp3-rDZgs2yZMF_FZ1hwIK1VhAy4UXswCtugaXEfJSoT_-k1u-qnoACsjxgF_ov93NaKMvdZzWc8vk0ofIzGxn5i-Y5bXn8yjOVQHGbDF9RMbdrTjgo2StZkU1iyrOvtKDLxt1_65HekSlAjBOgBskzCBSSoGVvHw",
    "executive_producer" : "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InVhUk9nbjc4U1ZSSzhzZE8zcEd4NCJ9.eyJpc3MiOiJodHRwczovL2hlbmRoLWZzbmQuZXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlZDJlNWRjOGM5YjAwMGMwOGJmY2I1MiIsImF1ZCI6IkNhc3RpbmciLCJpYXQiOjE1OTA4ODAzNTIsImV4cCI6MTU5MDk2Njc1MiwiYXpwIjoiUjlEQTdjWE0xbmZmcUdtRHdyWG40VjN4emdvN2Ryc0wiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.RK1s5LNfxMti-z2o2t9zkX1d7I6DlrX9DQIuREjVuzsZkC82q66oTUNQIRu3BwDUQkHUd8Ore3AsF8RtGhOtBNdtLuJUa3YW6r2bZa8aC393up357fIgp6SQq6DRZi-PNlu-9KCYz3-O0cNPaTwEIhc3I73nBB9RbvXcppxA72_EUOjRDJw_PImcHeRVWlZZZut-d7-YSFM-4cU-4vG0Bm5UFOScboOZQPcuK7cB8rD_ESJOfLwtgrmYulMEzKlF7vbPI5TeKVv0G7dbIBNz-yVVLnWBn9zNPS5RjRaDQ0dxufrJO7CJtdTavhDSm_4OmtdOoixgcEoPwFCXdCnIEQ"
}

casting_assistant_auth_header = {
    'Authorization': bearer_tokens['casting_assistant']
}

casting_director_auth_header = {
    'Authorization': bearer_tokens['casting_director']
}

executive_producer_auth_header = {
    'Authorization': bearer_tokens['executive_producer']
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
        response = self.client().post('/movies', json=self.a_movie, headers = executive_producer_auth_header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_create_a_movie_fails_422_error(self):
        response = self.client().post('/movies', json=self.an_invalid_movie, headers = executive_producer_auth_header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_create_a_movie_fails_401_error(self):
        response = self.client().post('/movies', json=self.a_movie, headers = casting_director_auth_header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_create_an_actor(self):
        response = self.client().post('/actors', json=self.an_actor, headers = casting_director_auth_header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_create_an_actor_fails_422_error(self):
        response = self.client().post('/actors', json=self.an_invalid_actor, headers = casting_director_auth_header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_create_an_actor_fails_401_error(self):
        response = self.client().post('/actors', json=self.an_invalid_actor, headers = casting_assistant_auth_header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)

    '''
    GET Endpoints
    '''

    def test_get_movies(self):

        response = self.client().get('/movies', headers = casting_assistant_auth_header)
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

        response = self.client().get('/actors', headers = casting_assistant_auth_header)
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
        response = self.client().patch('/movies/1', json=self.an_updated_movie, headers = casting_director_auth_header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_update_a_movie_fails_404_error(self):
        response = self.client().patch('/movies/444', json=self.an_updated_movie, headers = casting_director_auth_header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_update_a_movie_fails_401_error(self):
        response = self.client().patch('/movies/444', json=self.an_updated_movie, headers = casting_assistant_auth_header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_update_an_actor(self):
        response = self.client().patch('/actors/10', json=self.an_updated_actor, headers = casting_director_auth_header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_update_an_actor_fails_404_error(self):
        response = self.client().patch('/actors/444', json=self.an_updated_actor, headers = casting_director_auth_header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_update_an_actor_fails_401_error(self):
        response = self.client().patch('/actors/444', json=self.an_updated_actor, headers = casting_assistant_auth_header)
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

        response = self.client().delete('/movies/{}'.format(movie_id), headers = executive_producer_auth_header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], "Movie record deletion completed")
        self.assertEqual(data['deleted'], movie_id)

    def test_delete_a_movie_fails_404_error(self):

        response = self.client().delete('/movies/444', headers = executive_producer_auth_header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_delete_a_movie_fails_401_error(self):

        response = self.client().delete('/movies/444', headers = casting_director_auth_header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_delete_an_actor(self):

        # Create a new actor to be deleted later
        actor = Actor(name="Hemilly", age="240", gender="Male", movie_id=1)
        actor.insert()
        actor_id = actor.id

        response = self.client().delete('/actors/{}'.format(actor_id), headers = casting_director_auth_header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], "Actor record deletion completed")
        self.assertEqual(data['deleted'], actor_id)

    def test_delete_an_actor_fails_404_error(self):

        response = self.client().delete('/actors/444', headers = casting_director_auth_header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_delete_an_actor_fails_401_error(self):

        response = self.client().delete('/actors/444', headers = casting_assistant_auth_header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)


if __name__ == "__main__":
    unittest.main()
