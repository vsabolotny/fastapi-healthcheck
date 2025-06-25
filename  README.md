# FastAPI Health Check Service

A minimal FastAPI application exposing a health check endpoint.

## Requirements

- Python 3.8+
- pip

## Installation

```bash
pip install fastapi uvicorn
```

## Running the Application

```bash
uvicorn main:app --reload
```

## API Endpoints
### GET /health
Returns a plain text health status.

Response:

```bash
health status is green
```

## License
MIT