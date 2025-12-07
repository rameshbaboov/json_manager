from sqlalchemy import Column, BigInteger, String, DateTime
from sqlalchemy.sql import func
from app.db.base import Base


class Category(Base):
    __tablename__ = "category"

    id = Column(BigInteger, primary_key=True, autoincrement=True)

    # 3-level category structure
    category_level1 = Column(String(255), nullable=False)
    category_level2 = Column(String(255))
    category_level3 = Column(String(255))

    # 3 tags
    tag1 = Column(String(100))
    tag2 = Column(String(100))
    tag3 = Column(String(100))

    created_at = Column(DateTime, server_default=func.now(), nullable=False)
