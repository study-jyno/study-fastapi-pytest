from sqlalchemy.orm import scoped_session, sessionmaker
from app.database.core import SessionLocal

Session = scoped_session(SessionLocal)
