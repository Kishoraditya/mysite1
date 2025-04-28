# Wagtail CMS Project

A production-ready Wagtail CMS project with PostgreSQL integration, containerization, and automated testing.
A flexible landing page application built with Wagtail CMS.

## Features

- Wagtail CMS for content management
- PostgreSQL database integration
- Docker and Docker Compose for containerization
- Automated testing with pytest and coverage
- Health check endpoint
- Environment variable management
- Static analysis with flake8 and isort
- Fully customizable landing pages with modular components
- SEO optimization built-in
- Responsive design
- Accessibility compliant
- Performance optimized
- Docker deployment ready

## Requirements

- Python 3.8+
- PostgreSQL
- Docker and Docker Compose (for containerized deployment)

## Project Structure

```bash
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
│   │   └── 0001_initial.py
│   ├── models.py              # Page models
│   ├── static/
│   │   └── css/
│   │       └── home.css
│   ├── templates/             # HTML templates
│   │   └── home/
│   │       └── home_page.html
│   └── tests/                 # Tests for home app
│       └── test_home_page.py
├── landing/                   # Landing app
│   ├── migrations/            # Database migrations
│   │   └── 0001_initial.py
│   ├── models.py              # Page models
│   ├── static/
│   │   ├── css/
│   │   │    └── landing.css
│   │   └── js/
│   │       ├── modules/
│   │       │    ├──accessiblity.js
│   │       │    ├──lazyload.js
│   │       │    ├──performance.js
│   │       │    └──testimonials.js
│   │       ├── tests/
│   │       │    ├──performance.test.js
│   │       │    └──setup.js
│   │       ├──main.js
│   │       └── sw.js
│   ├── templates/             # HTML templates
│   │   └── landing/
│   │       ├── blocks/
│   │       │    ├── content_block.html
│   │       │    ├── cta_block.html
│   │       │    ├── feature_block.html
│   │       │    ├── features_block.html
│   │       │    ├── hero_block.html
│   │       │    ├── testimonial_block.html
│   │       │    └── testimonials_block.html
│   │       └── landing_page.html
│   ├── tests/                 # Tests for home app
│   │   ├── test_accessibility.py
│   │   ├── test_models.py
│   │   ├── test_seo.py
│   │   └── test_views.py
│   ├── admin.py  
│   ├── apps.py  
│   ├── views.py  
│   └── urls.py  
├── Makefile                   # Make commands
├── manage.py                  # Django management script
├── MANIFEST.in
├── mysite/                    # Project settings
│   ├── settings/              # Django settings
│   │   ├── base.py
│   │   ├── dev.py
│   │   └── production.py
│   ├── static/
│   ├── templates/             # Project templates
│   │   ├── 500.html
│   │   ├── 404.html
│   │   ├── robots.txt
│   │   ├── sitemap.xml
│   │   └── base.html
│   ├── tests/                 # Project tests
│   │   └── test_health_check.py
│   ├── urls.py                # URL configuration
│   └── wsgi.py                # WSGI configuration
├── pytest.ini                 # Pytest configuration
├── README.md                  # Project README
├── requirements.txt 
├── nginx/                    # Nginx setup
│   ├── conf.d/               # 
│   │   └── default.conf      # Coonfig file
├── search/                    # Search app
│   ├── templates/             # Search templates
│   │   └── search/
│   │       └── search.html
│   └── views.py               # Search views
└── setup.cfg                  # Configuration for linting tools
└── setup.py
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

6. Access the site at [http://localhost:8000](http://localhost:8000) and the admin at [http://localhost:8000/admin/](http://localhost:8000/admin/[)

## Docker Deployment

1. Make sure Docker and Docker Compose are installed on your system.

2. Create a `.env` file based on `.env.example`:

   ```bash
   cp .env.example .env
   ```

   Then edit the `.env` file with your production settings.

3. Generate SSL certificates for HTTPS:

   ```bash
   mkdir -p nginx/ssl
   openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout nginx/ssl/server.key -out nginx/ssl/server.crt
   ```

4. Build and start the containers:

   ```bash
   docker-compose up -d
   ```

5. Create a superuser:

   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

6. Visit [https://yourdomain.com/admin/](https://yourdomain.com/admin/) to access the Wagtail admin interface.

## Testing

### Type 1

1. Install test dependencies:

   ```bash
   pip install pytest pytest-django pytest-cov coverage
   ```

2. Run tests:

   ```bash
   pytest --cov=. --cov-report=html
   ```

3. View the coverage report in the `htmlcov` directory

For JavaScript tests:

```bash
npm test
```

### Type 2

Run tests with pytest:

```bash
make test
```

### Type 3

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

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Create it from Scratch

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

12. Access the site at [http://localhost:8000](http://localhost:8000) and the admin at [http://localhost:8000/admin/](http://localhost:8000/admin/)
