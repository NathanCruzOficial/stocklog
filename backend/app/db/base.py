
"""
StockLog - Database Base
------------------------
Define a estrutura-base compartilhada pelos modelos SQLAlchemy.

Responsabilidades:
- Centralizar os metadados da aplicação.
- Gerar identificadores UUID.
- Registrar datas de criação e atualização.
"""

# ============================================================
# IMPORTS
# ============================================================

import uuid

from sqlalchemy import DateTime, Uuid, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# ============================================================
# DECLARATIVE BASE
# ============================================================

class Base(DeclarativeBase):
    """Classe declarativa central dos modelos do sistema."""

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
