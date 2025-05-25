from .session import engine, Base
from .models import Transaction

def init_db():
    Base.metadata.create_all(bind=engine)