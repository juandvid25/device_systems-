from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# Importar Base y modelos
from app.database.connection import Base
from app.models import user_model, device_model, loan_model

config = context.config
if config.config_file_name:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata