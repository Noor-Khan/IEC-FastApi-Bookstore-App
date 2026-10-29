"""
Database setup for the Bookstore app.

This file connects the app to the database using SQLAlchemy. It:
- reads the database URL from the .env file,
- creates the engine (the actual connection to the database),
- creates a session factory used to talk to the database per request,
- defines `Base`, the parent class all ORM models inherit from,
- provides helpers to get a DB session (for FastAPI) and to create tables.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from dotenv import load_dotenv

import os


# Load variables from the .env file into the environment,
# so secrets like the DB URL aren't hard-coded in the source.
load_dotenv()

# Database connection string, e.g. postgresql://user:pass@host:5432/dbname
SQLALCHEMY_DATABASE_URL: str | None = os.getenv(key="SQLALCHEMY_DATABASE_URL")

# The engine manages the pool of connections to the database.
engine: Unknown = create_engine(SQLALCHEMY_DATABASE_URL)

# Factory that creates new DB sessions.
# autocommit=False: we commit changes explicitly, so nothing is saved by accident.
# autoflush=False: changes aren't sent to the DB until we choose to, giving more control.
SessionLocal: sessionmaker[Session] = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for ORM models; SQLAlchemy uses it to track all tables we define.
Base: Any = declarative_base()

def get_db():
    """
    Provide a database session for a single request.

    Input:  None (used as a FastAPI dependency via `Depends(get_db)`).
    Output: Yields a SQLAlchemy `Session` object.

    Why: Each request gets its own fresh session, and the `finally` block
    guarantees the session is closed afterwards (even if an error occurs),
    so connections are not leaked.
    """
    # Open a new session for this request.
    db: Session = SessionLocal()
    try:
        # Hand the session to the route; execution pauses here until the request is done.
        yield db
    finally:
        # Always close the session to return the connection to the pool.
        db.close()

def create_table():
    """
    Create all database tables defined by models inheriting from `Base`.

    Input:  None.
    Output: None (tables are created in the database as a side effect).

    Why: Lets the app set up its schema automatically on startup,
    without writing SQL `CREATE TABLE` statements by hand.
    """
    Base.metadata.create_all(bind=engine)