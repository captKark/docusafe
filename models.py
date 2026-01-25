# models.py
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False) # <--- MUST BE HERE
    password = Column(String, nullable=False)           # <--- MUST BE HERE
    experience_years = Column(Integer)
    status = Column(String, default="Intern")
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    documents = relationship("Document", back_populates="owner")
# --------------------------------------------
# New Document model
class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    # Foreign key relationship to User
    # It says: the number in this column must exist in the users.id column
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # Relationship to User model
    # magic link: this lets us say - document.owner to get the User object
    owner = relationship("User", back_populates="documents")