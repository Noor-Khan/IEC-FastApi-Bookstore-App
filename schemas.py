"""
Pydantic schemas for the Bookstore app.

Schemas define the shape of data going in and out of the API.
FastAPI uses them to validate request bodies and format responses.
They are separate from the SQLAlchemy models (database tables) so the
API contract can differ from how data is stored.
"""

from pydantic import BaseModel

class BookBase(BaseModel):
    """
    Fields shared by every book schema.

    Why: Keeps common fields in one place so the create and response
    schemas don't repeat them.
    """
    title: str
    description: str
    auth: str  # author of the book
    year: int  # publication year

class BookCreate(BookBase):
    """
    Data the client sends when creating a new book.

    Why: No `id` here, because the database generates it.
    """
    pass  # same fields as BookBase, nothing extra needed

class Book(BookBase):
    """
    Book data returned to the client in API responses.

    Why: Adds the database-generated `id` and lets Pydantic read
    directly from SQLAlchemy model objects.
    """
    id: int
    class config:
        # Allow building this schema from ORM objects (e.g. a SQLAlchemy Book row)
        # instead of only from dicts.
        orm_mode = True  # Pydantic v1 name for this setting
        from_attribute= True  # Pydantic v2 name for this setting

