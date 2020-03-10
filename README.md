# grapinator
Dynamic GraphQL API Creator for Python

## Introduction
Grapinator is a dynamic api generator based on the [Graphene](http://graphene-python.org) library for building GraphQL query services.  All you have to do to get a fully fuctional GraphQL service up and running is to configure a few setup files!  

## Key Features
- **No coding required:** Utilizes Python metaprogramming so no additional coding is required to implement new GraphQL services!
- **Built with Flask-SQLAlchemy:** Code based on the [SQLAlchemy + Flask Tutorial](http://docs.graphene-python.org/projects/sqlalchemy/en/latest/tutorial/) examples.
- **Runtime configuration:** Runtime configuration is managaged using the [grapinator.ini](grapinator/resources/grapinator.ini) file. 
- **Flexable GraphQL schema definition:** All Graphene and database information is provided by a [Python dictionary](grapinator/resources/schema.dct) that you change for your needs. Please review the [schema documentation](docs/schema_docs.md).
- **Additional query logic:** More robust query logic has been added giving the api consumer more options to query for specific data.

## Licensing
This project is licensed under the [BSD 3-clause](License.txt) license.

## Contributing
Allthough I use this code in production at my company, I consider it alpha code.  If you have any ideas, just open an issue and tell me what you think, how it may be improved, bugs you may find, etc.

## Getting Started

### Demo Prerequisites
- [docker](https://docs.docker.com/install/)
- [docker-compose](https://docs.docker.com/compose/install/) 

### Employee database demo setup
- **Note:** Startup the first time will take a bit longer as the employee database is created on initial load.  Look for "Database employeesdb setup complete." in the output of docker-compose before you continue.  Once the contaner is started you can start the [GraphiQL IDE](https://localhost:8443/employees/gql)
```
docker/docker_build_grapinatordb
docker-compose -f docker/grapinator.yml up
```

### Development setup

#### Start employees db
```
docker-compose -f docker/grapinatordb.yml up
```

#### Setup OSX/Linux
```
python -m venv venv
source venv/bin/activate
(venv) $ export $(cat .env)
(venv) $ pip install -r requirements.txt
(venv) $ python setup.py develop
(venv) $ cd grapinator;python app.py
```

#### Setup Windows
```
python -m venv venv
venv\Scripts\activate.bat
(venv) pip install -r requirements.txt
(venv) python setup.py develop
(venv) set GQLAPI_CRYPT_KEY=[get key from .env]
(venv) cd grapinator
(venv) python app.py
```

#### Running unit tests from the command line
Unit tests are located in the 'tests' directory.
Integration tests are located in the 'tests_integration' directory.
```
python -m unittest [filename]
```
