# Technical Test Template

## MIO Added exercises
### Tasks:
- Add a new alert code: Implement a new alert code that checks if a user has made more than five transactions (deposits or withdrawals) within a 1-minute window. This will test your ability to work with time windows and count transactions.
- User-specific Alerts: Allow for custom alert thresholds based on user profiles or risk ratings.
- Implement data persistence: Currently, the application does not store any data. Implement data persistence using a database like SQLite or PostgreSQL. This will test your ability to work with databases and ORMs like SQLAlchemy.

## CODING TEST COMMENTS
- Instructions to run the application and tests are the same as in the skeleton project (see below).
- To limit the scope of the coding test/exercise:
   - In the code only used libraries installed in the skeleton project provided. 
   - application implements an in-memory database, which means that data will be lost when the server restarts.

## Getting started

We have set up a basic Flask API that runs on port `5000` and included a `pytest` test showing the endpoint working.

If you prefer to use FastAPI, Django or other Python packages, feel free to add any you want using Poetry.
We have included a `Makefile` for conveince but you are free to run the project however you want.

### Requirements

- Python 3.12
- [Poetry](https://python-poetry.org/docs/) for dependency management

### Install dependencies

```sh
poetry install
```

### Start API server

```sh
make run
```

### Run tests

```sh
make test
```

## Testing

```sh
curl -XPOST 'http://127.0.0.1:5000/event' -H 'Content-Type: application/json' \
-d '{"type": "deposit", "amount": "217.00", "user_id": 11, "time": 35}'
```
