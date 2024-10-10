import os
import importlib
from sqlalchemy import create_engine
from alembic.config import Config as AlembicConfig
from alembic import command
from user_monitoring.models.base import Base
from user_monitoring.config import Config


def import_all_models():
    models_package = importlib.import_module("user_monitoring.models")
    for attr_name in dir(models_package):
        if not attr_name.startswith("__"):
            getattr(models_package, attr_name)


def setup_alembic(db_uri: str) -> AlembicConfig:
    alembic_cfg = AlembicConfig("alembic.ini")
    return alembic_cfg


def create_or_update_database():
    if Config.DB_URI is None:
        raise ValueError("DB_URI environment variable is not set")

    db_uri = Config.DB_URI
    print(f"Using DB_URI: {db_uri}")

    # Import all models to ensure they're registered with Base
    import_all_models()

    # Create an engine
    engine = create_engine(db_uri, echo=True)

    # Set up Alembic
    alembic_cfg = setup_alembic(db_uri)

    # Check if the database exists
    if not os.path.exists(db_uri.replace('sqlite:///', '')):
        # If the database doesn't exist, create it and all tables
        Base.metadata.create_all(engine)
        print(f"Database created at {db_uri}")

        # After creating the database, stamp it with the 'base' revision
        command.stamp(alembic_cfg, "head")
    else:
        print(f"Database already exists at {db_uri}")

    # Generate a new migration if there are changes
    try:
        command.revision(alembic_cfg, autogenerate=True, message="Auto-generated migration")
        print("New migration created")
    except Exception as e:
        print(f"No new migrations needed: {e}")

    # Upgrade the database to the latest migration
    command.upgrade(alembic_cfg, "head")
    print("Database upgraded to the latest version")


if __name__ == "__main__":
    create_or_update_database()
