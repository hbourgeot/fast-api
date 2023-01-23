from pydantic import BaseModel
from datetime import date, time
from typing import Optional


class Empleado(BaseModel):
  __tablename__ = "empleado"
  cedula: int
  nombre: str
  apellido: str
  direccion: str
  correo: str
  telefono: str
  fecha_contratacion: date


class Promotor(BaseModel):
  codigo: int
  cedula_empleado: int


class Proyecto(BaseModel):
  codigo: int
  nombre: str
  denominacion_comercial: str
  estado_actual: str


class Tarea(BaseModel):
  codigo: int
  descripcion: str
  duracion_estimada: time
  duracion_real: time
  fecha_real: date
  fecha_estimada: date
  tipo: str
  codigo_proyecto: Optional[int]


class Documento(BaseModel):
  codigo: int
  documento_especificacion: str
  codigo_fuente: int
  descripcion: str
  tipo: str
  codigo_tareas: int


class Version(BaseModel):
  codigo: int
  fecha: date
  descripcion: str
  codigo_documentos: int


class EmpleadoTarea(BaseModel):
  id: int
  codigo_tareas: int
  cedula_empleado: int


class EmpleadoProyecto(BaseModel):
  id: int
  codigo_proyecto: int
  cedula_empleado: int
