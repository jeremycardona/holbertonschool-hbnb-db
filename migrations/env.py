# env.py

from alembic import context
from sqlalchemy import engine_from_config, pool
from logging.config import fileConfig

from src import app, db  # Import your Flask application and SQLAlchemy instance

config = context.config

# Use your Flask app's config to get the SQLAlchemy database URI
config.set_main_option('sqlalchemy.url', app.config['SQLALCHEMY_DATABASE_URI'])

# Ensure Alembic can work with your SQLAlchemy engine
engine = engine_from_config(
    config.get_section(config.config_ini_section),
    prefix='sqlalchemy.',
    poolclass=pool.NullPool,
)

# This ensures that Alembic uses the correct metadata from your SQLAlchemy models
with app.app_context():
    db.init_app(app)
    target_metadata = db.Model.metadata

# Add your target metadata to the Alembic config
config.set_main_option('sqlalchemy.target_metadata', target_metadata)

# Ensure Alembic imports your models
# `target_metadata` should contain the metadata of all your SQLAlchemy models
# This assumes all your models are imported into `target_metadata`
from src.models import *  # Import all your SQLAlchemy models here

# This function should return the `target_metadata` defined above
def run_migrations_online():
    """
    Run migrations in 'online' (non-stored) mode.
    """
    # ... Existing code ...

    return context.configure(
        url=config.get_main_option("sqlalchemy.url"),
        target_metadata=target_metadata,
        literal_binds=True,
        **current_app.extensions['migrate'].configure_args
    )

# Call the `run_migrations_online` function
if context.is_offline_mode():
    # ... Existing code ...
else:
    # Call the `run_migrations_online` function
    run_migrations_online()

