from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base


engine = create_engine("sqlite:///authors.db")
Base.metadata.create_all(engine)
Base.metadata.bind = engine
Session = sessionmaker(bind=engine)
session = Session()
