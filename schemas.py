from database import Base
from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer, Date, String, Time


class Empleado(Base):
  cedula = Column(Integer, primary_key=True)  # int
  nombre = Column(String(60))                 # varchar
  apellido = Column(String(60))
  direccion = Column(String(60))
  correo = Column(String(120))
  telefono = Column(String(22))
  fecha_contrato = Column(Date)               # date


class Promotor(Base):
  id = Column(Integer, primary_key=True)
  cedula_empleado = Column(ForeignKey("empleado.cedula"))


class Proyectos(Base):
  codigo = Column(Integer, primary_key=True)
  nombre = Column(String(60))
  denominacion_comercial = Column(String(60))
  estado_actual = Column(String(60))


class Tareas(Base):
  codigo = Column(Integer, primary_key=True)
  descripcion = Column(String(60))
  duracion_estimada = Column(Time)
  duracion_real = Column(Date)
  fecha_real = Column(Date)
  fecha_estimada = Column(Date)
  tipo = Column(String(60))


class EmpleadoTareas(Base):
  id = Column(Integer, primary_key=True)
  codigo_tarea = Column(ForeignKey("tareas.codigo"))      # foreign key
  cedula_empleado = Column(ForeignKey("empleado.cedula"))
