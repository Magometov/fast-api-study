from sqlalchemy import BigInteger, CheckConstraint, SmallInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from src.core.db.base import SAModel


class User(SAModel):
    __tablename__ = "users"
    __table_args__ = (CheckConstraint("age >= 18", name="age_range_constraint"),)
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str | None] = mapped_column(String(length=20))
    age: Mapped[int | None] = mapped_column(SmallInteger)
    wallet_address: Mapped[str | None] = mapped_column(String(length=48), unique=True)
