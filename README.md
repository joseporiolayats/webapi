# WebAPI code assessment
#### Backend API service using Python
This is a webapp backend service created for the sole purpose of exploring some
API use-cases following Python best practices and being as broad and modern as
possible so to be compliant with the requirements and also able to further
extend its capabilities.

##  Capabilities
This app is able to provide the following:

-[x] Get user data filtered by user ID. Accessed by roles "users" and "admin"
-[x] Get user data filtered by user name. Accessed by roles "users" and "admin"
-[x] Get the list of policies linked to a user name. Accessed by role "admin"
-[x] Get the user linked to a policy number. Accessed by role "admin"

## License
- All the software is opensource and free for personal and commercial use, except MongoDB Atlas which is a service running in a free tier.
- Authentication and authorization. Take the user role from the web
- service that returns the
  list of company clients.

## Documentation
Click [here](https://joseporiolayats.github.io/webapi) to access the full
documentation.
It is deployed in Github Pages through MKDocs automatic documentation for python projects.

## CI/CD workflow
It is configured for manual auto-testing, linting and documentation deployment through GitHub Actions.

## Virtualization
This project is virtualized using [Poetry](www.python-poetry.org)
To install poetry run:
```commandline
curl -sSL https://install.python-poetry.org | python3 -
```

## Data workflow
It uses MongoDB as the main database for cold storage and operations, and the module also suports using a cached version of the data
(currently not fully implemented)

In order to work with MongoDB Atlas there is a signup needed and one can use the free tier database, which is a managed database running on AWS.
visit [mongodb.org](www.mongodb.org)

## Reproducibility
As it's using poetry for virtualization, it also uses poetry for package management.
The current versions are locked so that all works as intended.

## How to install
First clone the repository
```commandline
git clone https://github.com/joseporiolayats/webapi
```

Supposing you installed poetry, go into the main directory of the project and type
```commandline
poetry install
```
This command will install all the required packages. You will also have a venv available.

Then you will need to create a .env file in the main directory.
It has to look like this:
```python
# .env
DB_URL=mongodb+srv://[username]@[clustername].wjfxjp0.mongodb.net/test
DB_NAME=webapiDB
DB_COLLECTION_CLIENTS=clients
DB_COLLECTION_POLICIES=policies
DB_CLIENTS=https://www.mocky.io/v2/5808862710000087232b75ac
DB_POLICIES=https://www.mocky.io/v2/580891a4100000e8242b75c5
```
The DB_URL variable is given by MongoDB Atlas service

## Tech stack
This project makes use of the following main technologies:
- Python 3.11.2
- FastAPI, for serving the API endpoints
- MongoDB, for storing and manipulating the data.
- MongoDB Atlas, cloud hosting for managed database (free tier)
- Uvicorn, webserver

## Usage
Run the main.app file and the webapi service will open
```commandline
python main.py
```

## API endpoints
I use the package httpie, which is easy and capable for handling RESTful requests from the console.
```commandline
pip install httpie
```

There are several endpoints implemented in order to fulfill the requisites of the assessment.
- Authentication
  - users/register user=MyEmail password=MyPassword
  - users/login user=MyEmail password=MyPassword
  - users/me token=MyToken

### Login use case
```commandline
http POST localhost:8000/users/login email="britneyblankenship@quotezart.com"
password="a0ece5db-cd14-4f21-812f-966633e7be86"
```
Which returns
```json
HTTP/1.1 200 OK
content-length: 200
content-type: application/json
date: Mon, 08 May 2023 08:37:15 GMT
server: uvicorn

{
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2ODM1MzcxMzUsImlhdCI6MTY4MzUzNTAzNSwic3ViIjoiYTBlY2U1ZGItY2QxNC00ZjIxLTgxMmYtOTY2NjMzZTdiZTg2In0.ejLX9eno6b5bxWPR296M_AvWiTMzPXPpJWBnw11_g94"
}
```
Then you can copy the token and use it for accessing the restricted areas.
```commandline
http GET http://localhost:8000/policies Authorization:"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2ODM1MzcxMzUsImlhdCI6MTY4MzUzNTAzNSwic3ViIjoiYTBlY2U1ZGItY2QxNC00ZjIxLTgxMmYtOTY2NjMzZTdiZTg2In0.ejLX9eno6b5bxWPR296M_AvWiTMzPXPpJWBnw11_g94"

```

## Future work
This project could be drastically improved by adding a frontend, like React or Next.js.
