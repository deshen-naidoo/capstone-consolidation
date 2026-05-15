# Capstone Project: News Application

A robust Django web application featuring a Custom User Model, RESTful API, MariaDB integration, and automated testing.

## Prerequisites
- Python 3.9+
- MariaDB Server (must be running locally on port 3306)

## Installation Instructions

1. **Database Setup**
   Ensure your local MariaDB instance is running. 
   Create the database by running: `CREATE DATABASE news_db;`

2. **Virtual Environment & Dependencies**
   `python3 -m venv venv`
   `source venv/bin/activate`
   `python3 -m pip install -r requirements.txt`

3. **Database Migrations**
   Because SQLite components have been removed, you must run migrations to populate the MariaDB tables:
   `python3 manage.py makemigrations news`
   `python3 manage.py migrate`

4. **Run the Application**
   `python3 manage.py runserver`

The application will now safely load on the default path: `http://localhost:8000/`

## Testing
To run the comprehensive REST API test suite, run:
`python3 manage.py test news`