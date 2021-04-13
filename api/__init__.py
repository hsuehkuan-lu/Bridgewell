from app import app

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine


DATABASE_URI = 'sqlite:///dsp_rtb.db'
# DATABASE_URI = 'mysql+pymysql://root:qq456789@127.0.0.1:3306/dsp_rtb'
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI

#       --- DATABASE ---
engine = create_engine(
    DATABASE_URI
)
connection = engine.connect()
SESSION = sessionmaker(autocommit=False, autoflush=False, bind=engine)
SCOPED_SESSION = scoped_session(SESSION)

db = SQLAlchemy(app)
Base = declarative_base()
Base.query = SCOPED_SESSION.query_property()


from api import models, views

db.create_all()
