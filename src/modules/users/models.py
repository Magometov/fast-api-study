from src.core.db.base import SAModel
from sqlalchemy.orm import Mapped, mapped_column 
from sqlalchemy import BigInteger, String, SmallInteger, CheckConstraint

class User(SAModel):
    __tablename__ = 'users'
    __table_args__ = (
        CheckConstraint('age >= 18', name='age_range_constraint'),
    )
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(length=20))
    age: Mapped[int] = mapped_column(SmallInteger)
