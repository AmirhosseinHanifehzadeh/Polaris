# Measurements API - Getting Started Guide

## Overview

This guide shows you how to run the Measurements API and view logs for the GET measurements endpoints.

## Prerequisites

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Database Setup**
   - The application is configured to use MySQL with PyMySQL
   - Make sure you have the `cryptography` package installed (already added to requirements.txt)
   - If using Docker, the MySQL database will be automatically set up

## Running the Application

### Option 1: Using the Enhanced Server Script (Recommended)

```bash
python run_server.py
```

This script provides:
- Enhanced logging configuration
- Clear endpoint information
- Better error handling

### Option 2: Using Django Management Command

```bash
python manage.py runserver 0.0.0.0:8000
```

### Option 3: Using Docker

```bash
docker-compose up
```

## API Endpoints

Once the server is running, you can access:

- **List Measurements**: `GET http://localhost:8000/measurements/`
- **Get Single Measurement**: `GET http://localhost:8000/measurements/{id}/`
- **Create Measurement**: `POST http://localhost:8000/measurements/`
- **Bulk Create**: `POST http://localhost:8000/measurements/bulk_create/`
- **Delete Measurement**: `DELETE http://localhost:8000/measurements/{id}/`

## Testing the API

### Using the Test Script

```bash
python test_measurements.py
```

This script will:
1. Show expected logs
2. Test all GET endpoints
3. Display responses

### Using curl

```bash
# List all measurements
curl http://localhost:8000/measurements/

# List with pagination
curl "http://localhost:8000/measurements/?limit=5&offset=0"

# List with technology filter
curl "http://localhost:8000/measurements/?technology=LTE"

# List with date range
curl "http://localhost:8000/measurements/?start_date=2024-01-01T00:00:00Z&end_date=2024-12-31T23:59:59Z"

# Get single measurement
curl http://localhost:8000/measurements/1/
```

## Understanding the Logs

When you make requests to the GET measurements endpoints, you'll see logs like this:

### For List Measurements (`GET /measurements/`)

```
INFO 2025-08-21 06:25:23,767 apps.measurements.views:list:35 --> Processing list request with params: {'limit': '100', 'offset': '0'}
DEBUG 2025-08-21 06:25:23,768 apps.measurements.views:list:55 --> Executing list_measurements with filters: technology=None, start_date=None, end_date=None, limit=100, offset=0
DEBUG 2025-08-21 06:25:23,769 django.db.backends:execute:99 --> (0.001) SELECT COUNT(*) AS "__count" FROM "measurements"; args=()
DEBUG 2025-08-21 06:25:23,770 django.db.backends:execute:99 --> (0.002) SELECT "measurements"."id", "measurements"."timestamp", ... FROM "measurements" ORDER BY "measurements"."timestamp" DESC LIMIT 100 OFFSET 0; args=()
INFO 2025-08-21 06:25:23,771 apps.measurements.views:list:65 --> Successfully retrieved 0 measurements out of 0 total
INFO 2025-08-21 06:25:23,772 django.server:log_message:154 --> "GET /measurements/ HTTP/1.1" 200 1234
```

### For Get Single Measurement (`GET /measurements/{id}/`)

```
INFO 2025-08-21 06:25:24,123 apps.measurements.views:retrieve:25 --> Processing retrieve request for measurement ID: 1
DEBUG 2025-08-21 06:25:24,124 django.db.backends:execute:99 --> (0.001) SELECT "measurements"."id", "measurements"."timestamp", ... FROM "measurements" WHERE "measurements"."id" = 1 LIMIT 21; args=(1,)
WARNING 2025-08-21 06:25:24,125 apps.measurements.views:retrieve:30 --> Measurement with ID 1 not found
INFO 2025-08-21 06:25:24,126 django.server:log_message:154 --> "GET /measurements/1/ HTTP/1.1" 404 45
```

## Log Levels Explained

- **INFO**: General information about request processing
- **DEBUG**: Detailed information about database queries and parameter parsing
- **WARNING**: Non-critical issues (e.g., measurement not found)
- **ERROR**: Critical errors that prevent request completion

## Troubleshooting

### PyMySQL Authentication Error

If you see this error:
```
RuntimeError: 'cryptography' package is required for sha256_password or caching_sha2_password auth methods
```

Solution:
```bash
pip install cryptography==42.0.8
```

### Database Connection Issues

If you're using Docker and see database connection errors:

1. Make sure the database container is running:
   ```bash
   docker-compose ps
   ```

2. Check if the database is healthy:
   ```bash
   docker-compose logs db
   ```

3. Run migrations:
   ```bash
   python manage.py migrate
   ```

### Empty Results

If you get empty results, it means there are no measurements in the database. You can create some test data using the POST endpoints.

## Creating Test Data

To see actual data in the logs, create some test measurements:

```bash
# Create a single measurement
curl -X POST http://localhost:8000/measurements/ \
  -H "Content-Type: application/json" \
  -d '{
    "timestamp": "2024-01-15T10:30:00Z",
    "latitude": 40.7128,
    "longitude": -74.0060,
    "technology": "LTE",
    "rsrp": -85.5,
    "rsrq": -12.3,
    "download_rate": 45.2,
    "upload_rate": 12.8
  }'

# Create multiple measurements
curl -X POST http://localhost:8000/measurements/bulk_create/ \
  -H "Content-Type: application/json" \
  -d '{
    "measurements": [
      {
        "timestamp": "2024-01-15T10:30:00Z",
        "latitude": 40.7128,
        "longitude": -74.0060,
        "technology": "LTE",
        "rsrp": -85.5,
        "rsrq": -12.3
      },
      {
        "timestamp": "2024-01-15T10:31:00Z",
        "latitude": 40.7129,
        "longitude": -74.0061,
        "technology": "LTE",
        "rsrp": -87.2,
        "rsrq": -13.1
      }
    ]
  }'
```

## Log Files

The application creates detailed logs in:
- Console output (real-time)
- `detailed_logs.log` file (persistent)

You can monitor the log file in real-time:
```bash
tail -f detailed_logs.log
```

## API Documentation

For complete API documentation, see the Swagger specification at:
`apps/measurements/swagger.yml`

You can also view it in a Swagger UI by visiting:
`http://localhost:8000/measurements/` (if you have Swagger UI configured) 