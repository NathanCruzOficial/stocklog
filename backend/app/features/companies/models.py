
"""
Modelo de empresa do StockLog.

Define os dados cadastrais e a identificação de cada empresa
registrada no sistema.
"""

# Imports
import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

# TYPE_CHECKING é utilizado para evitar importações circulares
if TYPE_CHECKING:
    from app.features.users.models import User


# Modelo
class Company(Base):
    """Representa uma empresa cadastrada no StockLog."""

    __tablename__ = "companies"

    # Identificação
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    # Dados cadastrais
    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    document: Mapped[str] = mapped_column(
        String(14),
        unique=True,
        nullable=False,
    )

    # Endereço
    zip_code: Mapped[str | None] = mapped_column(String(8), nullable=True)
    street: Mapped[str | None] = mapped_column(String(150), nullable=True)
    number: Mapped[str | None] = mapped_column(String(20), nullable=True)
    complement: Mapped[str | None] = mapped_column(String(100), nullable=True)
    neighborhood: Mapped[str | None] = mapped_column(String(100), nullable=True)
    city: Mapped[str | None] = mapped_column(String(100), nullable=True)
    state: Mapped[str | None] = mapped_column(String(2), nullable=True)

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

    # Relacionamento com usuários
    users: Mapped[list["User"]] = relationship(
        back_populates="company",
        cascade="all, delete-orphan",
    )