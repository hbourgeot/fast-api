from pydantic import BaseModel
from datetime import date
from database import Base

class Empleado(BaseModel):
  __tablename__ = "empleado"
  cedula: int
  nombre: str
  apellido: str
  direccion: str
  correo: str
  telefono: str
  contrato: str

