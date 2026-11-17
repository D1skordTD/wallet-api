from sqlalchemy import Column, Numeric
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class Wallet(Base):
    __tablename__ = "wallets"

    id = Column(PG_UUID(as_uuid=True), primary_key=True)
    balance = Column(Numeric(18, 2), nullable=False, default=0)
    