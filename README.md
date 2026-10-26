
# CampusFix — Campus Issue Management System

## Project Overview

CampusFix is a web application that helps manage campus maintenance
and student service requests through a central issue register.

## Objectives

- Provide a simple interface to report campus issues.
- Store submitted reports in an SQLite database.
- Track open, in-progress, and resolved issues.
- Search and filter reports.
- Provide a JSON API for issue records.
- Demonstrate containerization using Docker.

## Technology Stack

- Python
- Flask
- SQLite
- HTML5
- CSS3
- Docker

## Main Features

1. Submit a campus issue.
2. View all reports.
3. Search and filter reports.
4. Update issue status.
5. Delete reports.
6. View dashboard statistics.
7. Access issue data through a JSON API.
8. Check application health.

## Installation

Install Python 3.10 or later.

```bash
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000 in your browser.

## Docker Setup

Build the image:

```bash
docker build -t campusfix .
```

Run the container with persistent database storage:

```bash
docker run -d --name campusfix \
  -p 5000:5000 \
  -e DB_PATH=/data/campusfix.db \
  -v campusfix_data:/data \
  campusfix
```

Open http://localhost:5000.

## API Endpoints

GET /api/issues

Returns all issue records in JSON format.

GET /health

Returns the application health status.

## Database

SQLite stores issue titles, categories, locations, priorities,
statuses, reporter names, descriptions, and timestamps.

The database and sample records are initialized automatically.

## Conclusion

CampusFix demonstrates how a Python web application can combine
server-side programming, database operations, user input handling,
search, filtering, and Docker deployment.

## Future Enhancements

- User authentication
- Administrator and student roles
- Email notifications
- Issue assignment
- Reports and analytics
- Audit history
