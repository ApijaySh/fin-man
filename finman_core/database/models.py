from sqlalchemy import Column, Integer, Float, String
from .session import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    description = Column(String)
    payer = Column(String)
    type = Column(String)  # 'debit' or 'credit'