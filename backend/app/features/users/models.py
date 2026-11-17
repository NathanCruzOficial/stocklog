
"""
Modelo de usuário do StockLog.

Define os dados de identificação, autenticação e vínculo
do usuário com sua empresa.
"""

# Imports
import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

# TYPE_CHECKING é utilizado para evitar importações circulares
if TYPE_CHECKING:
    from app.features.companies.models import Company


# Modelo
class User(Base):
    """Representa um usuário cadastrado no StockLog."""

    __tablename__ = "users"

    # Identificação
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    # Dados pessoais
    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    cpf: Mapped[str] = mapped_column(
        String(11),
        unique=True,
        nullable=False,
    )

    # Dados de acesso
    email: Mapped[str] = mapped_column(
        String(254),
        unique=True,
        nullable=False,
    )

    password_hash: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    # Dados profissionais
    position: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    # Relacionamento com empresa
    company_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("companies.id"),
        nullable=False,
        index=True,
    )

    company: Mapped["Company"] = relationship(
        back_populates="users",
    )

    # Datas de controle
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
