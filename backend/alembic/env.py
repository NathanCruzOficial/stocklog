
"""
StockLog - Alembic Environment
------------------------------
Configuração do ambiente de migrações do banco de dados.

Responsabilidades:
- Carregar as configurações da aplicação.
- Disponibilizar os metadados dos modelos SQLAlchemy.
- Configurar migrações online e offline.
"""

# ============================================================
# IMPORTS
# ============================================================

# isort: skip_file

from logging.config import fileConfig

from alembic import context
from sqlalchemy import create_engine, pool

from app.core.config import get_settings
from app.db.base import Base
import app.db.models  # noqa: F401


# ============================================================
# ALEMBIC CONFIGURATION
# ============================================================


config = context.config
settings = get_settings()

# Configuração dos logs do Alembic
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadados utilizados na geração automática de migrações
target_metadata = Base.metadata


# ============================================================
# OFFLINE MIGRATIONS
# ============================================================

def run_migrations_offline() -> None:
    """
    Executa migrações sem estabelecer uma conexão com o banco.

    Gera instruções SQL utilizando a URL configurada na aplicação.
    """

    context.configure(
        url=settings.DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


# ============================================================
# ONLINE MIGRATIONS
# ============================================================

def run_migrations_online() -> None:
    """
    Executa migrações utilizando uma conexão ativa com o banco.

    Cria um engine temporário e associa sua conexão ao Alembic.
    """

    connectable = create_engine(
        settings.DATABASE_URL,
        poolclass=pool.NullPool,
    )

    try:
        with connectable.connect() as connection:
            context.configure(
                connection=connection,
                target_metadata=target_metadata,
                compare_type=True,
            )

            with context.begin_transaction():
                context.run_migrations()

    finally:
        connectable.dispose()


# ============================================================
# MIGRATION EXECUTION
# ============================================================

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
