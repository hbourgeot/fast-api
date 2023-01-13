from database import Base
from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer, Date, String, Time, Text


class Empleado(Base):
  __tablename__ = "empleado"
  cedula = Column(Integer, primary_key=True)  # int
  nombre = Column(String(60))                 # varchar
  apellido = Column(String(60))
  direccion = Column(String(60))
  correo = Column(String(120))
  telefono = Column(String(22))
  fecha_contratacion = Column(Date)               # date


class Promotor(Base):
  __tablename__ = "promotor"
  codigo = Column(Integer, primary_key=True)
  usuario = Column(String(20))
  contra = Column(String(16))
  cedula_empleado = Column(ForeignKey("empleado.cedula"))


class Proyectos(Base):
  __tablename__ = "proyectos"
  codigo = Column(Integer, primary_key=True)
  nombre = Column(String(60))
  denominacion_comercial = Column(String(60))
  estado_actual = Column(String(60))


class Tareas(Base):
  __tablename__ = "tareas"
  codigo = Column(Integer, primary_key=True)
  descripcion = Column(String(60))
  duracion_estimada = Column(Time)
  duracion_real = Column(Date)
  fecha_real = Column(Date)
  fecha_estimada = Column(Date)
  tipo = Column(String(60))


class Documentos(Base):
  codigo = Column(Integer, primary_key=True)
  documento_especificacion = Column(String(60))
  codigo_fuente = Column(Integer)
  descripcion = Column(Text)
  tipo = Column(String(60))
  codigo_tareas = Column(ForeignKey("tareas.codigo"))


class Version(Base):
  codigo = Column(Integer, primary_key=True)
  fecha = Column(Date)
  descripcion = Column(String(60))
  codigo_documentos = Column(ForeignKey("documentos.codigo"))


class EmpleadoTareas(Base):
  __tablename__ = "empleado_tareas"
  id = Column(Integer, primary_key=True)
  codigo_tarea = Column(ForeignKey("tareas.codigo"))      # foreign key
  cedula_empleado = Column(ForeignKey("empleado.cedula"))
