from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Datos de conexión
DATABASE_URL = "mysql+mysqlconnector://root:AlonsoChavez1234567@localhost/tienda_de_comics_proyecto"

# Crear motor de conexión
engine = create_engine(DATABASE_URL)

# Crear sesión local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para modelos
Base = declarative_base()
