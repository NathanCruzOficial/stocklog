
"""
Registro central dos modelos do StockLog.

Importa os modelos para disponibilizá-los na metadata
da classe Base utilizada pelo SQLAlchemy e Alembic.
"""

# Modelos dos domínios
from app.features.companies.models import Company
from app.features.users.models import User

# Os próximos modelos serão registrados aqui:

