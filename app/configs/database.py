from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
#from contextlib import contextmanager

# Connection URL format: dialect+driver://username:password@host:port/database
connection_url = URL.create(
    
    drivername = "sqlite",
    #username="your_username",
    #password="your_password",
    #host="localhost",
    #port=5432,
    database="app/db/aiproxys.db"
)

# Create engine with connection pooling
engine = create_engine(
    connection_url,
    pool_size = 5,
    max_overflow = 10,
    pool_pre_ping = True,  # Test connections for liveness
    echo = True  # Show SQL in logs (debug)
)


# Create session factory (2.0 style)
DBSession = sessionmaker(
    bind = engine,
    autoflush = False,
    expire_on_commit = False,
    future = True  # Enables 2.0 style
)

def get_db():
    db = DBSession()
    try:
        yield db
    finally:
        db.close()

"""
# Usage of Session
@contextmanager
def get_session()-> Generator[Session, None, None]:
    #Yield a session with automatic cleanup
    session = DBSession()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
"""

class Base(DeclarativeBase):
    pass

# ---- Create Database and Tables if not exists ----
#Base.metadata.create_all(bind = engine)