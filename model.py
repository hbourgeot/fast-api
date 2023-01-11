from pydantic import BaseModel
from datetime import date, time


class Empleado(BaseModel):
  __tablename__ = "empleado"
  cedula: int
  nombre: str
  apellido: str
  direccion: str
  correo: str
  telefono: str
  fecha_contrato: date


class Promotor(BaseModel):
  id: int
  usuario: str
  contra: str
  cedula_empleado: int


class Proyectos(BaseModel):
  codigo: int
  nombre: str
  denominacion_comercial: str
  estado_actual: str


class Tareas(BaseModel):
  codigo: int
  descripcion: str
  duracion_estimada: time
  duracion_real: time
  fecha_real: date
  tipo: str


class EmpleadoTareas(BaseModel):
  id: int
  codigo_tarea: int
  cedula_empleado: int


class EmpleadoProyecto(BaseModel):
  id: int
  codigo_proyecto: int
  cedula_empleado: int
