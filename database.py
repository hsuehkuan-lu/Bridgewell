from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from config import DATABASE_URI

#       --- DATABASE ---
engine = create_engine(
    DATABASE_URI
)
connection = engine.connect()
SESSION = sessionmaker(autocommit=False, autoflush=False, bind=engine)
SCOPED_SESSION = scoped_session(SESSION)

db = SQLAlchemy()
Base = declarative_base()
Base.query = SCOPED_SESSION.query_property()


def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import api.models
    Base.metadata.create_all(bind=engine)


init_db()
