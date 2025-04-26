# Wagtail CMS Project

A production-ready Wagtail CMS project with PostgreSQL integration, containerization, and automated testing.

## Features

- Wagtail CMS for content management
- PostgreSQL database integration
- Docker and Docker Compose for containerization
- Automated testing with pytest and coverage
- Health check endpoint
- Environment variable management
- Static analysis with flake8 and isort

## Project Structure

```
mysite/
├── conftest.py                # Pytest configuration
├── docker-compose.yml         # Docker Compose configuration
├── Dockerfile                 # Docker configuration
├── docs/                      # Documentation
│   ├── architecture.puml      # Architecture diagram
│   └── design_guidelines.md   # UI/UX design guidelines
├── .env                       # Environment variables (not in version control)
├── .env.example               # Example environment variables
├── .gitignore                 # Git ignore configuration
├── .dockerignore              # Docker ignore configuration
├── home/                      # Home app
│   ├── migrations/            # Database migrations
│   ├── models.py              # Page models
│   ├── templates/             # HTML templates
│   └── tests/                 # Tests for home app
├── Makefile                   # Make commands
├── manage.py                  # Django management script
├── mysite/                    # Project settings
│   ├── settings/              # Django settings
│   ├── templates/             # Project templates
│   ├── tests/                 # Project tests
│   └── urls.py                # URL configuration
├── pytest.ini                 # Pytest configuration
├── requirements.txt           # Python dependencies
├── search/                    # Search app
│   ├── templates/             # Search templates
│   └── views.py               # Search views
└── setup.cfg                  # Configuration for linting tools
```

## Local Setup

### Prerequisites

- Docker and Docker Compose
- Make (optional, for using Makefile commands)

### Setup Steps

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd mysite
   ```

2. Create a `.env` file based on `.env.example`:
   ```bash
   cp .env.example .env
   ```

3. Build and start the Docker containers:
   ```bash
   make build
   make run
   ```
   
   Or without Make:
   ```bash
   docker-compose build
   docker-compose up
   ```

4. Run migrations:
   ```bash
   make migrate
   ```
   
   Or without Make:
   ```bash
   docker-compose exec web python manage.py migrate
   ```

5. Create a superuser:
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

6. Access the site at http://localhost:8000 and the admin at http://localhost:8000/admin/

## Testing

Run tests with pytest:

```bash
make test
```

Or without Make:

```bash
docker-compose exec web pytest --cov=. --cov-report=html
```

View the coverage report in the `htmlcov` directory.

## Development Commands

- `make build`: Build Docker containers
- `make run`: Run the application
- `make test`: Run tests with pytest
- `make lint`: Run linting tools
- `make format`: Format code with isort and black
- `make migrate`: Run database migrations
- `make static`: Collect static files
- `make shell`: Open Django shell
- `make clean`: Remove Docker containers and volumes

## Deployment

For production deployment:

1. Set appropriate environment variables in `.env`
2. Build the Docker image
3. Run with the production settings:
   ```bash
   docker-compose exec web python manage.py runserver --settings=mysite.settings.production
   ```

## License

[Your License]
```

## How to Replicate (Local Setup)

1. Install Python 3.8 or higher
2. Install PostgreSQL
3. Install Wagtail:
   ```bash
   pip install wagtail
   ```
4. Create a new Wagtail project:
   ```bash
   wagtail start mysite
   cd mysite
   ```
5. Create a PostgreSQL database:
   ```bash
   psql -U postgres -c "DROP DATABASE IF EXISTS mysite;"
   psql -U postgres -c "CREATE DATABASE mysite;"
   ```
6. Create and configure all the files as shown above
7. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
8. Set up environment variables by creating a `.env` file based on `.env.example`
9. Run migrations:
   ```bash
   python manage.py migrate
   ```
10. Create a superuser:
    ```bash
    python manage.py createsuperuser
    ```
11. Run the development server:
    ```bash
    python manage.py runserver
    ```
12. Access the site at http://localhost:8000 and the admin at http://localhost:8000/admin/

## How to Test

1. Install test dependencies:
   ```bash
   pip install pytest pytest-django pytest-cov coverage
   ```
2. Run tests:
   ```bash
   pytest --cov=. --cov-report=html
   ```
3. View the coverage report in the `htmlcov` directory

## Project Structure

```
mysite/
├── conftest.py
├── docker-compose.yml
├── Dockerfile
├── docs/
│   ├── architecture.puml
│   └── design_guidelines.md
├── .env
├── .env.example
├── .gitignore
├── .dockerignore
├── home/
│   ├── migrations/
│   │   └── 0001_initial.py
│   ├── models.py
│   ├── static/
│   │   └── css/
│   │       └── home.css
│   ├── templates/
│   │   └── home/
│   │       └── home_page.html
│   └── tests/
│       └── test_home_page.py
├── Makefile
├── manage.py
├── MANIFEST.in
├── mysite/
│   ├── settings/
│   │   ├── base.py
│   │   ├── dev.py
│   │   └── production.py
│   ├── static/
│   ├── templates/
│   │   └── base.html
│   ├── tests/
│   │   └── test_health_check.py
│   ├── urls.py
│   └── wsgi.py
├── pytest.ini
├── README.md
├── requirements.txt
├── search/
│   ├── templates/
│   │   └── search/
│   │       └── search.html
│   └── views.py
├── setup.cfg
└── setup.py
