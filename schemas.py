from database import Base
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.types import Integer, Date, String, Time, Text


class Empleado(Base):
  __tablename__ = "empleado"
  cedula = Column(Integer, primary_key=True)  # int
  nombre = Column(String(60))                 # varchar
  apellido = Column(String(60))
  direccion = Column(String(60))
  correo = Column(String(120))
  telefono = Column(String(22))
  fecha_contratacion = Column(Date)           # date


class Promotor(Base):
  __tablename__ = "promotor"
  codigo = Column(Integer, primary_key=True)
  cedula_empleado = Column(Integer, ForeignKey("empleado.cedula"))
  codigo_proyecto = Column(Integer, ForeignKey("proyectos.codigo"))
  empleado = relationship("Empleado")


class Proyecto(Base):
  __tablename__ = "proyectos"
  codigo = Column(Integer, primary_key=True)
  nombre = Column(String(60))
  denominacion_comercial = Column(String(60))
  estado_actual = Column(String(60))
  empleado_proyecto = relationship("EmpleadoProyecto")
  promotor_proyecto = relationship("Promotor")
  tarea = relationship("Tarea")


class Tarea(Base):
  __tablename__ = "tareas"
  codigo = Column(Integer, primary_key=True)
  descripcion = Column(String(60))
  duracion_estimada = Column(Time)
  duracion_real = Column(Date)
  fecha_real = Column(Date)
  fecha_estimada = Column(Date)
  tipo = Column(String(60))
  codigo_proyecto = Column(Integer, ForeignKey("proyectos.codigo"))
  empleado_tarea = relationship("EmpleadoTarea")


class Documento(Base):
  __tablename__ = "documentos"
  codigo = Column(Integer, primary_key=True)
  documento_especificacion = Column(String(60))
  codigo_fuente = Column(Integer)
  descripcion = Column(Text)
  tipo = Column(String(60))
  codigo_tareas = Column(ForeignKey("tareas.codigo"))
  version = relationship("Version")


class Version(Base):
  __tablename__ = "version"
  codigo = Column(Integer, primary_key=True)
  fecha = Column(Date)
  descripcion = Column(String(60))
  codigo_documentos = Column(Integer, ForeignKey("documentos.codigo"))


class EmpleadoTarea(Base):
  __tablename__ = "empleado_tareas"
  id = Column(Integer, primary_key=True)
  codigo_tareas = Column(Integer, ForeignKey("tareas.codigo"))      # foreign key
  cedula_empleado = Column(Integer, ForeignKey("empleado.cedula"))
  empleado = relationship("Empleado")


class EmpleadoProyecto(Base):
  __tablename__ = "empleado_proyectos"
  id = Column(Integer, primary_key=True)
  codigo_proyecto = Column(Integer, ForeignKey("proyectos.codigo"))
  cedula_empleado = Column(Integer, ForeignKey("empleado.cedula"))
  empleado = relationship("Empleado")
