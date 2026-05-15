# News Application - Capstone Project

A comprehensive Django application featuring custom user roles, RESTful APIs, MariaDB integration, Sphinx documentation, and Docker containerisation.

## Running the Application Locally (Virtual Environment)

1. **Clone the repository:**
   `git clone https://github.com/deshen-naidoo/capstone-consolidation.git`
   `cd capstone-consolidation/news_project`

2. **Set up the virtual environment:**
   `python3 -m venv venv`
   `source venv/bin/activate`

3. **Install dependencies:**
   `pip install -r requirements.txt`

4. **Database Setup (MariaDB):**
   Ensure MariaDB is running locally on port 3306. Create a database named `news_db`. Update the `DATABASES` credentials in `news_project/settings.py` to match your local database user/password.

5. **Migrate and Run:**
   `python3 manage.py makemigrations news`
   `python3 manage.py migrate`
   `python3 manage.py runserver`

   The web application will load on port 8000: `http://localhost:8000/`

## Running via Docker

1. Ensure Docker Desktop is running.
2. Build the Docker image:
   `docker build -t news-app .`
3. Run the container:
   `docker run -dp 8000:8000 news-app`

*(Note: The Docker container expects a connection to a MariaDB database as defined in settings.py).*

## Documentation
HTML documentation generated via Sphinx can be found in `docs/_build/html/index.html`.
