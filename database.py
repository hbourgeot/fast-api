# Imports
import pymysql
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# enlace de la base de datos, antes del '://' se indica qué base de datos se usa con cual conector de python
DATABASE_URL = "mysql+pymysql://root:Wini.h16b.@localhost:3306/testing"

engine = create_engine(DATABASE_URL)  # configurar la conexión con la base de datos
SesionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)  # crear la sesion local
Base = declarative_base()  # crear la base del esquema de la base de datos
