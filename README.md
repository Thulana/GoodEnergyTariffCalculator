# Good Energy Tariff Calculator API 

[![Build](https://github.com/Thulana/GoodEnergyTariffCalculator/actions/workflows/build.yml/badge.svg?branch=main)](https://github.com/Thulana/GoodEnergyTariffCalculator/actions/workflows/build.yml)

Good Energy Tariff Calculator is a flask microservice for calculating tariff for local consumers in germany

| 	                           | 	                              |
|-----------------------------|--------------------------------|
| **Type**                	   | flask REST microservice 	      |
| **Python Version**          | 3.9                          	 |
| **Flask Version**         	 | 2.0.1               	          |
| **Authentication**          | Token based authentication     |
| **Persistence**             | SQLite                         |

## Table Of Contents

1. [Motivation](#motivation)
2. [API Documentation](#api-documentation)
3. [Getting Started](#getting-started)
   1. [Docker](#via-docker-manually)
   2. [Local](#locally)
      1. [Virtual Environment](#virtual-environment)
      2. [Dependency Installation](#dependency-installation)
      3. [Setting up Database](#setting-up-sqlite3-database)
      4. [Running the Application](#running-the-application)
   3. [Data sourcing](#data-sourcing)
4. [Developer Notes](#developer-notes)
    1. [Environment Setup](#environment-setup)
       1. [Environment Variables](#environment-variables)
       2. [Database](#database)
       3. [Python](#python)
    2. [Testing](#testing)
    3. [Continuous Integration](#continuous-integration)
5. [Developer Checklist](#developer-checklist)
8. [References](#references)

## Motivation

Providing an API interface to calculate tariff on the fly

## API Documentation
| REST Endpoint        	              | Description                  	         |
|-------------------------------------|----------------------------------------|
| `POST /api/auth/register`        	  | Register new user in the system        | 
| `POST /api/auth/login`        	     | Generate a token for API authentication | 
| `GET /api/user/<username>`        	 | Retrieve user by username              | 
| `POST /api/price/tariff`        	   | Calculate tariff                       |

* Postman collection is available on path `/postman`
* NOTE: API will require registering and login to proceed with protected endpoint

## Getting Started

### Via docker manually

Issue following commands from root folder of the project
(This will use the location_prices.csv for data sourcing)

* Build : `docker build -t <image-name> -f infrastructure/docker/Dockerfile .`
* Run: `docker run -p 5000:5000 -td tariff_calc`

Environment variables defined in refer: [Environment Variables](#environment-variables)* can be provided like below. (If not provided, will fallback to default)

* Run: `docker run -e DATABASE_URL=<database_url> -p 5000:5000 -td <image-name>`

### locally

#### Virtual Environment

It is preferred to create a virtual environment for project. Once you install [virtual env](https://virtualenv.pypa.io/en/stable/installation/), inside the 
project.

```bash
python3 -m venv .venv
```

#### Dependency installation

To install the necessary packages:

```bash
source venv/bin/activate
pip3 install -r requirements.txt
```

This will install the required packages within your venv.

---

#### Setting up SQLite3 Database
####(SQLite3 is used for demonstration purposes. For production required a central MySQL/ Postgres database)

Database migrations are handled through Flask's Migrate Package. Migrations are used for updating and creating necessary tables/entries in your database.

To setup a SQLite3 database, navigate to the folder where `good_energy_tariff_calc.py` is located and run:

```bash
export FLASK_APP=good_energy_tariff_calc.py
```

To create database

```bash
flask db migrate "Create database"
```

To migrate changes

```bash
flask db upgrade
```

#### Running the Application

Use following commands to start service in development environment.

*Note: Needs to have environment variables exposed. refer: [Environment Variables](#environment-variables)*

```bash
export FLASK_APP=good_energy_tariff_calc.py
```

You can go ahead and run the application with a simple command:

```bash
flask run
```

### Data sourcing

For production, CSV file should be imported from a different method to the database. For demonstration
purpose, following command can be used to populate the database with a local csv file or file URL.

```bash
FLASK_APP=good_energy_tariff_calc flask import_prices <file path or URL>
```

## Developer Notes

### Environment setup

#### Environment Variables

Following environment variables will be used by the service.

| Variable Name        	                           | Description                  	    | Defaults |
|--------------------------------------------------|-----------------------------------|-----------|
| `DATABASE_URL`        	                           | SQLite database url               | /app.db |
| `JWT_SECRET_KEY`                                       | secret key for JWT generation     | my_precious_jwt |
| `SECRET_KEY`                                       | secret for signing session cookie | my_precious |

* For development creating `.env` file with above environment variables is enough.
* If not provided default configuration will be used

#### Database

* SQLite database
* Custom SQL dialect as default dialect is not supported due to SQLite limitations
* Hibernate as the ORM (persistence framework)

#### Python

* Python 3.9 is recommended

### Testing

Utilize unit test to provide proper test harness.

* unittest framework
* Execute the tests via `python3 -m unittest discover -s app/tests/`

### Continuous Integration

* Project is version controlled and available in GitHub
* Automated Build pipeline for build and test the service

## Developer Checklist

* [x] Static code analysis integration
* [ ] Add Swagger documentation 
* [ ] Improve data persistence ( Postgres or MySQL database )
* [ ] Cloud deployment configuration (kube) and infrastructure versioning (Helm)

## References

* Flask - https://flask.palletsprojects.com/en/2.0.x/
* Database migrations - https://flask-migrate.readthedocs.io/
* JWT authentication - https://flask-jwt-extended.readthedocs.io/en/stable/



