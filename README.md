# Practice Flask

Exercise to practice building a Flask API.

## Description
API endpoint called `/event` that receives a payload representing a user's action (like a deposit or withdrawal). Based on the activity in the payload, the endpoint checks against some predefined rules to determine if an alert should be raised.

The payload format:
```json
{
   "type": "deposit",
   "amount": "42.00",
   "user_id": 1,
   "time": 10
}
```
where
- type: str The type of user action, either deposit or withdraw.
- amount: str The amount of money the user is depositing or withdrawing.
- user_id: int A unique identifier for the user.
- time: int The timestamp of the action (this value is always increasing).

The response format:
```json
{
   "alert": true,
   "alert_codes": [30, 123],
   "user_id": 1
}
```

### Alert codes
- Code: 1100 : A withdrawal amount over 100
- Code: 30 : The user makes 3 consecutive withdrawals
- Code: 300 : The user makes 3 consecutive deposits where each one is larger than the previous
deposit (withdrawals in between deposits can be ignored).
- Code: 123 : The total amount deposited in a 30-second window exceeds 200

### Expected behaviour
The endpoint checks for these conditions to trigger alerts:
- alert: Should be true if any alert codes are triggered, otherwise false.
- alert_codes: A list of alert codes that have been triggered (if any)
- user_id: The user_id of the user whose action was processed

### ToDo exercises
- DONE: Add a new alert code: Implement a new alert code that checks if a user has made more than five transactions (deposits or withdrawals) within a 1-minute window.
- User-specific Alerts: Allow for custom alert thresholds based on user profiles or risk ratings.
- Implement data persistence: Currently, the application does not store any data. Implement data persistence using a database like SQLite or PostgreSQL. This will test your ability to work with databases and ORMs like SQLAlchemy.

## How to run

The Flask API runs on port `5000`.

There is a `Makefile` with a `run` command to start the application. It also has a `test` command to run the `pytest` test and check that the endpoint working.

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
curl -XPOST 'http://127.0.0.1:5000/event' -H 'Content-Type: application/json' -d '{"type": "deposit", "amount": "217.00", "user_id": 11, "time": 35}'
```
