"""
Database models for the Bookstore app.

Models are Python classes that map to database tables (SQLAlchemy ORM).
Each class is a table and each attribute is a column, so we can read and
write rows as normal Python objects instead of writing raw SQL.
"""

from db import Base
from sqlalchemy import Integer, Column, String

class Book(Base):
    """
    ORM model for the "Books" table.

    Why: Represents one book row in the database. Inheriting from `Base`
    (defined in db.py) registers the table so `create_table()` can build it.
    """
    # Name of the table in the database
    __tablename__ = "Books"

    # Unique identifier for each book; primary key is auto-incremented and indexed for fast lookups
    id: Column(Integer, primary_key=True, index=True)
    # Book title; indexed to speed up searching by title
    title: Column(String, index=True)
    # Short summary of the book; indexed for faster searching
    description: Column(String, index=True)
    # Author of the book; indexed for faster searching
    auth: Column(String, index=True)
    # Year the book was published (no index, we don't search by it)
    year: Column(Integer)
