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
- **type** (str) The type of user action, either deposit or withdraw.
- **amount** (str): The amount of money the user is depositing or withdrawing.
- **user_id** (int): A unique identifier for the user.
- **time** (int): The timestamp of the action (this value is always increasing).

The response format:
```json
{
   "alert": true,
   "alert_codes": [30, 123],
   "user_id": 1
}
```

### Alert codes
- **Code 1100** : A withdrawal amount over 100
- **Code 30** : The user makes 3 consecutive withdrawals
- **Code 300** : The user makes 3 consecutive deposits where each one is larger than the previous
deposit (withdrawals in between deposits can be ignored).
- **Code 123** : The total amount deposited in a 30-second window exceeds 200

### Expected behaviour
The endpoint checks for these conditions to trigger alerts:
- **alert**: Should be true if any alert codes are triggered, otherwise false.
- **alert_codes**: A list of alert codes that have been triggered (if any)
- **user_id**: The user_id of the user whose action was processed

### TODO Exercises
#### Add a new alert code (DONE)
Implement a new alert code that checks if a user has made more than five transactions (deposits or withdrawals) within a 1-minute window return code 500.

#### User-specific alerts (DONE)
Allow for custom alert thresholds to be based on user profiles or risk ratings.
Users can be defined in the database with levels of risk: low, medium and high.
If user is not found in the database, the risk level is medim.

If user risk level is:
- **low**: multiply the AMOUNT_LIMIT (or COUNT_LIMIT if no amount defined) that triggers the alert by 2.
- **medium**: use the limits defined
- **high:** divide the AMOUNT_LIMIT (or COUNT_LIMIT if no amount defined) that triggers the alert by 2 taking floor result and add 1.

#### Implement data persistence (DONE)
Use SQLAlchemy to handle a physical/persistent database (SQLite, PostgreSQL)

#### Add get endpoint (DONE)
Given a userId in the Url path, retrieve actions from that user.

#### RESTful endpoints
Convert API to RESTful
- `POST /api/v1/events`: Create a new event, and returns the event_id and alert_id (or null if no alert) with status code 201 when created
- `GET /api/v1/events/<event_id>`: Retrieve a specific event
- `GET /api/v1/alerts`: List all alerts
- `GET /api/v1/alerts/<alert_id>`: Retrieve a specific alert

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

### Setup the database with Alembic
Alembic is a database migration tool that:
- Tracks changes to your database schema
- Maintains version history
- Allows rollback of changes

With Alembic package installed, initialize migrations running command:
```bash
    alembic init migrations
```
Command creates `migrations` folder where stores the migrations.
In the base folder, edit the `alembic.ini` file:
- `script_location`: should be set to `migrations` if this was the name in previous command
- `sqlalchemy.url`: define your database connection string. ex: sqlite:///relative/path/to/file.db

In the migrations folder, edit `env.py` and set the `target_metadata` line to the `Base` in your project
```python
    from user_monitoring.models.base import Base
    ...
    target_metadata = Base.metadata
```
Create migration scripts (if database should be created in a folder, ensure it exists):
```bash
    alembic revision --autogenerate -m "your migration message"
```
If there are already tables created in the database your add the imports in `env.py` so Alembic can see them.
```python
    from user_monitoring.models.user_action_model import UserActionModel
```

Review the migrations generated in `migrations\versions` folder

Then, once happy with the script changes, run the following command to upgrade the database:
```bash
    alembic upgrade head
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

