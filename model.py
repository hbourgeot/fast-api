from pydantic import BaseModel
from datetime import date
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
  codigo: Optional[int]
  cedula_empleado: int
  codigo_proyecto: int


class Proyecto(BaseModel):
  codigo: Optional[int]
  nombre: str
  denominacion_comercial: str
  estado_actual: str


class Tarea(BaseModel):
  codigo: Optional[int]
  descripcion: str
  duracion_estimada: str
  duracion_real: str
  fecha_real: date
  fecha_estimada: date
  tipo: str
  codigo_proyecto: Optional[int]


class Documento(BaseModel):
  codigo: Optional[int]
  documento_especificacion: str
  codigo_fuente: str
  descripcion: str
  tipo: str
  codigo_tareas: int


class Version(BaseModel):
  codigo: Optional[int]
  fecha: date
  descripcion: str
  codigo_documentos: int


class EmpleadoTarea(BaseModel):
  id: Optional[int]
  codigo_tareas: int
  cedula_empleado: int


class EmpleadoProyecto(BaseModel):
  id: Optional[int]
  codigo_proyecto: int
  cedula_empleado: int


class Usuario(BaseModel):
  usuario: str
  password: str
