# JOTA News API

A RESTful API for news management built with Django and Django REST Framework. The system supports different user profiles, JWT authentication, and column-based access control.

## Features

- JWT-based authentication
- User management with different access levels (Admin, Employee, Client)
- News article management with draft/published states
- Column-based access control for news articles
- PostgreSQL database integration
- Automated testing with pytest
- Docker support for easy deployment

## Getting Started

### Prerequisites

- Docker and Docker Compose

### Installation & Setup

1. Create a `.env` file in the root directory with the following variables:
```
SECRET_KEY=your_django_secret_key
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=postgres
```

2. Build and start the containers:
```bash
docker-compose up --build
```

The application will:
- Start PostgreSQL database
- Run database migrations
- Execute tests
- Start the Django development server

The API will be available at `http://localhost:8000`

## Project Structure

Key files and their purposes:

- `docker-compose.yaml` - Defines services (PostgreSQL and Django app)
- `Dockerfile` - Instructions for building the Django application container
- `entrypoint.sh` - Container startup script that waits for PostgreSQL and runs migrations
- `initialize_database.sh` - Database initialization script
- `pytest.ini` - pytest configuration for running tests

## Testing

Tests are automatically run when the container starts. To run tests manually:

```bash
docker-compose exec django_app python -m pytest
```

## User Types

1. Employee with Admin (`is_admin=True`):
   - Full access to all users and articles
   - Can create/edit/delete any content

2. Regular Employee (`is_admin=False`):
   - Can create articles
   - Can edit/delete their own articles
   - Can edit their own user profile

3. Client User:
   - Can view published articles based on their plan
   - Can edit their own user profile
   - Cannot create/edit/delete articles

## Reference Values

### User Profiles
- `"EMP"` - Employee
- `"CLI"` - Client

### Plans
- `"INFO"` - JOTA Info (access to all non-column articles)
- `"PRO"` - JOTA PRO (access to specific columns)

### Article Columns
- `"POW"` - Power
- `"TAX"` - Taxes
- `"HLTH"` - Health
- `"EN"` - Energy
- `"LAB"` - Labor

### Article Status
- `"DRAF"` - Draft
- `"PUBD"` - Published

## Development Notes

The project uses:
- Python 3.11
- Django 4.2.19
- PostgreSQL 17
- pytest for testing
- JWT for authentication
