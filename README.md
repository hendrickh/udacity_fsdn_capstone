# Motivations & Covered Topics
This is the final project within the Udacity Full Stack Nanodegree Course, and it covers all the topics completed. Specifically this project will include the following technical topics:

1. Database modeling with SQLAlchemy.
2. Designing API endpoints to perform CRUD Operations on the DB via the Flask app.
3. Authentication & Authorization via Role Based Access Control (RBAC) with Auth0
4. Automated testing of the API endpoints (including the RBAC tests)
5. Deployment of the application to Heroku

# Context
The project brief is described below:

> The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process.

# Database Models
There are two tables configured for this project: 'Actor' and 'Movie'.

The 'Movie' table has the following columns configured:
1. id (Integer, Primary Key) - the main identifier for movies
2. title (String) - the title of the movie
3. release_date (Date) - the release date of the movie
4. actors - Links to the 'Actor' table

The 'Actor' table has the following columns configured:
1. id (Integer, Primary Key) - the main identifier for actors
2. name (String) - the name of the actor
3. age (Integer) - the age of the actor
4. gender (String) - the gender of the actor
5. movie_id (Integer, Foreign Key) - links to the 'Movie' table

The above information is high-leveled, and more detailed information can be inferred from the 'models.py' file.

# API Endpoints

### GET '/movies'
```bash
- Retrieves the list of movies in the database. It also includes the relevant actors details.
- Required roles: Casting Assistant, Casting Director, Executive Producer
- Required payload: None
- Sample output:
    {
        "movies": [
            {
                "actors": [
                    {
                        "age": 54,
                        "gender": "F",
                        "id": 5,
                        "movie_id": 2,
                        "name": "Emilly Herrell"
                    }
                ],
                "id": 2,
                "release_date": "Tue, 05 May 2020 00:00:00 GMT",
                "title": "Emilly and the Angry Horse - the Sequel"
            }
        ],
        "success": true
    }
```

### GET '/actors'
```bash
- Retrieves the list of actors in the database.
- Required roles: Casting Assistant, Casting Director, Executive Producer
- Required payload: None
- Sample output:
    {
        "actors": [
            {
                "age": 54,
                "gender": "F",
                "id": 5,
                "movie_id": 2,
                "name": "Emilly Herrell"
            }
        ],
        "success": true
    }
```

### POST '/movies'
```bash
- Creates a movie record in the database.
- Required roles: Executive Producer
- Required payload:
    {
        "title": "Emilly and the Angry Horse",
        "release_date": "2020-05-05"
    }
- Sample output:
    {
        "created": 3,
        "new_movie": {
            "actors": [],
            "id": 3,
            "release_date": "Tue, 19 May 2020 00:00:00 GMT",
            "title": "Emilly and the Angry Horse - the Sequel"
        },
        "success": true
    }
    Note that the "created" key refers to the movie id created.
```

### POST '/actors'
```bash
- Creates an actor record in the database.
- Required roles: Casting Director, Executive Producer
- Required payload:
    {
        "name": "Emilly Herrell",
        "age": 54,
        "gender": "F",
        "movie_id": 1
    }
- Sample output:
    {
        "created": 6,
        "new_actor": {
            "age": 54,
            "gender": "F",
            "id": 6,
            "movie_id": 1,
            "name": "Emilly Herrell"
        },
        "success": true
    }

    Note that the "created" key refers to the actor id created.
```

### PATCH '/movies/<int:id>'
```bash
- Update a movie record in the database.
- Required roles: Casting Director, Executive Producer
- Required payload:
    {
        "title": "Emilly and the Angry Horse",
        "release_date": "2020-05-05"
    }
    Note that you would need to specify the movie id in the API endpoint to patch the movie with that id.
- Sample output:
    {
        "message": "Movie record update completed",
        "success": true
    }
```

### PATCH '/actors/<int:id>'
```bash
- Update an actor record in the database.
- Required roles: Casting Director, Executive Producer
- Required payload:
    {
        "name": "Emilly Herrell",
        "age": 54,
        "gender": "F",
        "movie_id": 1
    }
    Note that you would need to specify the actor id in the API endpoint to patch the actor with that id.
- Sample output:
    {
        "message": "Actor record update completed",
        "success": true
    }
```

### DELETE '/movies/<int:id>'
```bash
- Delete a movie record in the database.
- Required roles: Executive Producer
- Required payload: None. Note that you would need to specify the movie id in the API endpoint to patch the movie with that id.
- Sample output:
    {
        "deleted": 3,
        "message": "Movie record deletion completed",
        "success": true
    }
```

### DELETE '/actors/<int:id>'
```bash
- Delete an actor record in the database.
- Required roles: Casting Director, Executive Producer
- Required payload: None. Note that you would need to specify the actor id in the API endpoint to patch the actor with that id.
- Sample output:
    {
        "deleted": 6,
        "message": "Actor record deletion completed",
        "success": true
    }
```

# Authentication
There are 3 roles configured for this project:
1. Casting Assistant
    * Can view the list of actors and movies in the DB
2. Casting Director
    * All permissions a Casting Assistant has
    * Add/delete an actor from the DB
    * Modify actors and movies
3. Executive Producer
    * All permissions a Casting Director has
    * Add/delete a movie from the DB

To avoid cluttering in this file, the JWT tokens for the 3 roles have been included in the 'test_app.py' file.

# Starting the Project Locally
The list of environment variables required to run the project locally can be seen in the 'setup.sh' file. This includes:
1. DATABASE_URL - the local database URL
2. AUTH0_DOMAIN - the Auth0 configured within Auth0 GUI
3. ALGORITHMS - the Auth0's algorithm configured within Auth0 GUI
4. API_AUDIENCE - the Auth0's API Audience configured within Auth0 GUI

To start the project, open up the terminal and change the working directory to this project's. Proceed by running the command below:
```bash
pip install -r requirements.txt
source setup.sh; flask run
```

# Running the tests locally
To run the tests locally, please run the following command:
```bash
source setup.sh; python -m unittest test_app.py
```

# Information for Udacity Project reviewers
The Heroku base URL for the project is - https://udacity-fsdn-capstone.herokuapp.com/

To test the API endpoints manually, please use the relevant JWT tokens included in the 'test_app.py' file.