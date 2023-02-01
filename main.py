# Local
import schemas
from database import SesionLocal, engine, Base
from estructuras import Lista, Pila
import model
# FastAPI
from fastapi import FastAPI, Depends, Body
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
# SQLAlchemy
from sqlalchemy.orm import Session

app = FastAPI()

origins = ["*"]

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["GET", "POST", "PATCH", "DELETE"],
  allow_headers=["*"]
)

Base.metadata.create_all(bind=engine)

# Abrimos la conexion con la base de datos

connection: Session


def obtener_bd():               # creamos la conexión con la base de datos
  global connection
  try:
    connection = SesionLocal()
    return connection
  finally:
    connection.close()

# Operaciones de proyectos


@app.get("/")
def home(db: Session = Depends(obtener_bd)):
  try:
    # Obtenemos todo de la base de datos
    proyectos = db.query(schemas.Proyecto).all()
    empleados = db.query(schemas.Empleado).all()
    tareas = db.query(schemas.Tarea).all()
    documentos = db.query(schemas.Documento).all()
    versiones = db.query(schemas.Version).all()

    return {
      "estado": "exitoso",
      "proyectos": proyectos,
      "empleados": empleados,
      "tareas": tareas,
      "documentos": documentos,
      "versiones": versiones
    }
  except Exception as e:
    raise HTTPException(500, str(e))


@app.get("/proyectos")
def mostrar_proyectos(db: Session = Depends(obtener_bd)):
  try:
    # definimos una lista
    proyectos_activos = Lista()
    proyectos_inactivos = Lista()

    # obtenemos los datos de la bd usando subconsultas: SELECT * FROM proyectos
    activos = db.query(schemas.Proyecto.estado_actual)\
      .filter(schemas.Proyecto.estado_actual == "Activo").scalar_subquery()

    proyectos = db.query(schemas.Proyecto).filter(schemas.Proyecto.estado_actual.in_(activos)).all()
    for proyecto in proyectos:  # iteramos el objeto
      proyectos_activos.agregar_final(proyecto)  # empujamos por

    inactivos = db.query(schemas.Proyecto.estado_actual)\
      .filter(schemas.Proyecto.estado_actual != "Activo").scalar_subquery()

    proyectos = db.query(schemas.Proyecto).filter(schemas.Proyecto.estado_actual.in_(inactivos)).all()
    for proyecto in proyectos:
      proyectos_inactivos.agregar_frente(proyecto)

    activos = proyectos_activos.retornar_datos()
    inactivos = proyectos_inactivos.retornar_datos()
    respuesta = {"activos": activos, "inactivos": inactivos}

    del proyectos_activos, proyectos_inactivos  # borramos la variable para liberar memoria

    return {"cantidad": len(respuesta), "proyectos": respuesta}
  except Exception as e:
    raise HTTPException(500, str(e))


@app.post("/crear/proyecto")
def agregar_proyecto(proyecto: model.Proyecto = Body(...), db: Session = Depends(obtener_bd)):
  try:
    db_proyecto = db.query(schemas.Proyecto).filter(schemas.Proyecto.codigo == proyecto.codigo).first()
    if db_proyecto:
      raise HTTPException(404, "El proyecto ya existe")

    del db_proyecto

    codigo = len(db.query(schemas.Proyecto).all()) + 1
    nuevo_proyecto = schemas.Proyecto(codigo=codigo, nombre=proyecto.nombre,
                                      denominacion_comercial=proyecto.denominacion_comercial,
                                      estado_actual=proyecto.estado_actual,
                                      )     # creamos al nuevo proyecto
    db.add(nuevo_proyecto)                                    # lo agregamos a la bd
    db.commit()                                               # confirmamos la inserción
    db.refresh(nuevo_proyecto)                                # refrescamos los valores en la variable

    return {"estado": "exitoso", "proyecto": nuevo_proyecto}  # retornamos al nuevo proyecto
  except Exception as e:
    raise HTTPException(400, str(e))


# noinspection PyTypeChecker
@app.patch("/modificar/proyecto/{proyecto_id}")
def actualizar_proyecto(proyecto_id: int, proyecto: model.Proyecto = Body(...), db: Session = Depends(obtener_bd)):
  try:
    # creamos la consulta de proyecto y comprobamos que existe dicho proyecto
    consulta_proyecto = db.query(schemas.Proyecto).filter(schemas.Proyecto.codigo == proyecto_id)
    db_proyecto = consulta_proyecto.first()

    if not db_proyecto:
      raise HTTPException(404, "Proyecto no encontrado")

    # asignamos los datos a actualizar y actualizamos estos
    proyecto.codigo = proyecto_id
    actualizar = proyecto.dict(exclude_unset=True)
    consulta_proyecto.filter(schemas.Proyecto.codigo == proyecto_id).update(actualizar, synchronize_session=False)
    db.commit()              # confirmamos cambios
    db.refresh(db_proyecto)  # refrescamos la variable con los valores actualizados

    return {"estado": "exitoso", "proyecto": db_proyecto}
  except Exception as e:
    raise HTTPException(400, str(e))


@app.get("/proyecto/{proyecto_id}")
def mostrar_proyecto(proyecto_id: int, db: Session = Depends(obtener_bd)):
  try:
    proyecto = db.query(schemas.Proyecto).get(proyecto_id)  # SELECT * FROM proyectos WHERE codigo = proyecto_id

    if not proyecto:
      raise HTTPException(404, "Proyecto no encontrado")

    return {"proyecto": proyecto}  # retornamos el proyecto
  except Exception as e:
    raise HTTPException(400, str(e))

# Operaciones de tareas


@app.get("/proyecto/{proyecto_id}/empleados")
def empleados_del_proyecto(proyecto_id: int, db: Session = Depends(obtener_bd)):
  try:
    proyecto = db.query(schemas.Proyecto).filter(schemas.Proyecto.codigo == proyecto_id).first()
    if not proyecto:
      raise HTTPException(404, "Proyecto no encontrado")

    empleados_pila = Pila()
    empleados = db.query(schemas.EmpleadoProyecto.cedula_empleado)\
      .filter(schemas.EmpleadoProyecto.codigo_proyecto == proyecto_id).scalar_subquery()

    empleados_proyecto = db.query(schemas.Empleado).filter(schemas.Empleado.cedula.in_(empleados))

    for empleado in empleados_proyecto:
      empleados_pila.apilar(empleado)

    respuesta = empleados_pila.retornar_datos()

    del empleados_pila, proyecto

    return {"cantidad": len(respuesta), "empleados": respuesta}
  except Exception as e:
    raise HTTPException(400, str(e))


@app.get("/proyecto/{proyecto_id}/tareas")
def mostrar_tareas_del_proyecto(proyecto_id: int, db: Session = Depends(obtener_bd)):
  try:
    proyecto = db.query(schemas.Proyecto).filter(schemas.Proyecto.codigo == proyecto_id).first()
    if not proyecto:
      raise HTTPException(404, "Proyecto no encontrado")

    tareas_lista = Lista()
    tareas = db.query(schemas.Tarea).filter(schemas.Tarea.codigo_proyecto == proyecto_id)

    for tarea in tareas:
      tareas_lista.agregar_final(tarea)

    respuesta = tareas_lista.retornar_datos()

    del proyecto, tareas_lista

    return {"cantidad": len(respuesta), "tareas": respuesta}
  except Exception as e:
    raise HTTPException(400, str(e))


@app.get("/tareas")
def mostrar_tareas(db: Session = Depends(obtener_bd)):
  try:
    tareas_lista = Lista()
    tareas = db.query(schemas.Tarea).all()

    for tarea in tareas:
      tareas_lista.agregar_final(tarea)

    respuesta = tareas_lista.retornar_datos()

    del tareas_lista

    return {"cantidad": len(respuesta), "tareas": respuesta}
  except Exception as e:
    raise HTTPException(400, str(e))


@app.post("/proyecto/{proyecto_id}/crear/tarea")
def agregar_tarea(proyecto_id: int, tarea: model.Tarea = Body(...), db: Session = Depends(obtener_bd)):
  try:
    proyecto = db.query(schemas.Proyecto).filter(schemas.Proyecto.codigo == proyecto_id).first()
    if not proyecto:
      raise HTTPException(404, "Proyecto no encontrado")

    db_tarea = db.query(schemas.Tarea).filter(schemas.Tarea.codigo == tarea.codigo).first()
    if db_tarea:
      raise HTTPException(400, "La tarea existe")

    del db_tarea, proyecto

    codigo = len(db.query(schemas.Tarea).all()) + 1
    nueva_tarea = schemas.Tarea(codigo=codigo,
                                descripcion=tarea.descripcion,
                                duracion_estimada=tarea.duracion_estimada,
                                duracion_real=tarea.duracion_real,
                                fecha_real=tarea.fecha_real,
                                fecha_estimada=tarea.fecha_estimada,
                                tipo=tarea.tipo, codigo_proyecto=proyecto_id)        # creamos a la nueva tarea

    db.add(nueva_tarea)                                 # lo agregamos a la bd
    db.commit()                                         # confirmamos la inserción
    db.refresh(nueva_tarea)                             # refrescamos los valores en la variable
    return {"estado": "exitoso", "tarea": nueva_tarea}  # retornamos al nuevo empleado
  except Exception as e:
    raise HTTPException(400, str(e))


# noinspection PyTypeChecker
@app.patch("/proyecto/{proyecto_id}/tarea/{tarea_id}")
def modificar_tarea(proyecto_id: int, tarea_id: int, tarea: model.Tarea = Body(...), db: Session = Depends(obtener_bd)):
  try:
    proyecto = db.query(schemas.Proyecto).filter(schemas.Proyecto.codigo == proyecto_id).first()
    if not proyecto:
      raise HTTPException(404, "Proyecto no encontrado")

    del proyecto

    consulta_tarea = db.query(schemas.Tarea).filter(schemas.Tarea.codigo == tarea_id)
    db_tarea = consulta_tarea.first()

    if not db_tarea:
      raise HTTPException(404, "Tarea no encontrada")

    tarea.codigo_proyecto = proyecto_id
    actualizar = tarea.dict(exclude_unset=True)
    consulta_tarea.filter(schemas.Tarea.codigo == tarea_id).update(actualizar, synchronize_session=False)
    db.commit()
    db.refresh(db_tarea)

    return {"estado": "exitoso", "tarea": db_tarea}
  except Exception as e:
    raise HTTPException(400, str(e))


@app.get("/tarea/{tarea_id}")
def mostrar_tarea(tarea_id: int, db: Session = Depends(obtener_bd)):
  try:
    tarea = db.query(schemas.Tarea).filter(schemas.Tarea.codigo == tarea_id).first()

    if not tarea:
      raise HTTPException(404, "No existe la tarea")

    return {"tarea": tarea}
  except Exception as e:
    raise HTTPException(400, str(e))


@app.get("/tarea/{tarea_id}/empleados")
def empleados_de_la_tarea(tarea_id: int, db: Session = Depends(obtener_bd)):
  try:
    tarea = db.query(schemas.Tarea).filter(schemas.Tarea.codigo == tarea_id).first()
    if not tarea:
      raise HTTPException(404, "Tarea no encontrada")

    empleados_pila = Pila()
    empleados_tarea = db.query(schemas.Empleado)\
      .join(schemas.EmpleadoTarea, schemas.Empleado.cedula == schemas.EmpleadoTarea.cedula_empleado
            and schemas.Tarea.codigo == schemas.EmpleadoTarea.codigo_tareas)\
      .filter(schemas.EmpleadoTarea.codigo_tareas == tarea_id).all()

    for empleado in empleados_tarea:
      empleados_pila.apilar(empleado)

    respuesta = empleados_pila.retornar_datos()

    del empleados_pila, tarea

    return {"cantidad": len(respuesta), "empleados": respuesta}
  except Exception as e:
    raise HTTPException(400, str(e))

# Operaciones de documentos asociados a cierta tarea


@app.get("/tarea/{tarea_id}/docs")
def docs_tarea(tarea_id: int, db: Session = Depends(obtener_bd)):
  try:
    tarea = db.query(schemas.Tarea).filter(schemas.Tarea.codigo == tarea_id).first()
    if not tarea:
      raise HTTPException(404, "Tarea no encontrada")

    docs_pila = Pila()  # creamos una pila
    documentos = db.query(schemas.Documento).all()  # obtenemos todos los registros de empleado

    for documento in documentos:  # iteramos el objeto
      # apilamos el nombre y el apellido
      docs_pila.apilar(documento)

    respuesta = docs_pila.retornar_datos()

    del docs_pila, tarea

    return {"cantidad": len(respuesta), "documentos": respuesta}
  except Exception as e:
    raise HTTPException(400, str(e))


@app.post("/tarea/{tarea_id}/docs")
def crear_doc(tarea_id: int, documento: model.Documento, db: Session = Depends(obtener_bd)):
  try:
    tarea = db.query(schemas.Tarea).filter(schemas.Tarea.codigo == tarea_id).first()
    if not tarea:
      raise HTTPException(404, "Tarea no encontrada")

    doc = db.query(schemas.Documento).filter(schemas.Documento.codigo == documento.codigo).first()
    if doc:
      raise HTTPException(404, "Documento ya existe")

    del doc, tarea

    codigo = len(db.query(schemas.Documento).all()) + 1
    nuevo_doc = schemas.Documento(codigo=codigo,
                                  documento_especificacion=documento.documento_especificacion,
                                  codigo_fuente=documento.codigo_fuente,
                                  descripcion=documento.descripcion,
                                  tipo=documento.tipo,
                                  codigo_tareas=tarea_id)      # creamos al nuevo documento
    db.add(nuevo_doc)                                     # lo agregamos a la bd
    db.commit()                                           # confirmamos la inserción
    db.refresh(nuevo_doc)                                 # refrescamos los valores en la variable

    return {"estado": "exitoso", "documento": nuevo_doc}  # retornamos al nuevo documento
  except Exception as e:
    raise HTTPException(400, str(e))


@app.get("/docs/{doc_id}/versiones")
def versiones_del_documento(doc_id: int, db: Session = Depends(obtener_bd)):
  try:
    doc = db.query(schemas.Documento).get(doc_id)
    if not doc:
      raise HTTPException(404, "El documento no existe")

    versiones = db.query(schemas.Version).filter(schemas.Version.codigo_documentos == doc_id).all()
    versiones_lista = Lista()
    for version in versiones:
      versiones_lista.agregar_final(version)

    respuesta = versiones_lista.retornar_datos()

    del versiones_lista, doc

    return {"cantidad": len(respuesta), "versiones": respuesta}
  except Exception as e:
    raise HTTPException(500, str(e))


@app.post("/docs/{doc_id}/crear/version")
def crear_version(doc_id: int, version: model.Version = Body(...), db: Session = Depends(obtener_bd)):
  try:
    doc = db.query(schemas.Documento).get(doc_id)
    if not doc:
      raise HTTPException(404, "El documento no existe")

    ver = db.query(schemas.Version).get(version.codigo)
    if ver:
      raise HTTPException(400, "La versión ya existe")

    del ver, doc

    codigo = len(db.query(schemas.Version).all()) + 1
    db_version = schemas.Version(codigo=codigo, fecha=version.fecha,
                                 descripcion=version.descripcion,
                                 codigo_documentos=doc_id)
    db.add(db_version)
    db.commit()
    db.refresh(db_version)

    return {"estado": "exitoso", "version": db_version}

  except Exception as e:
    raise HTTPException(500, str(e))


@app.get("/empleados")
def obtener_empleados(db: Session = Depends(obtener_bd)):
  try:
    empleados_pila = Pila()  # creamos una pila
    empleados = db.query(schemas.Empleado).all()  # obtenemos todos los registros de empleado

    for empleado in empleados:  # iteramos el objeto
      # apilamos el nombre y el apellido
      empleados_pila.apilar(empleado)

    respuesta = empleados_pila.retornar_datos()

    del empleados_pila

    return {"cantidad": len(respuesta), "empleados": respuesta}
  except Exception as e:
    raise HTTPException(400, str(e))


@app.get("/empleado/{empleado_id}")
def obtener_empleado(empleado_id: int, db: Session = Depends(obtener_bd)):
  try:
    empleado = db.query(schemas.Empleado).get(empleado_id)  # SELECT * FROM empleado WHERE cedula = empleado_id

    if empleado is None:
      raise HTTPException(404, "El empleado no existe")

    return {"empleado": empleado}
  except Exception as e:
    raise HTTPException(400, str(e))


@app.post("/nuevo/empleado")
def crear_empleado(empleado: model.Empleado = Body(...), db: Session = Depends(obtener_bd)):
  try:
    db_empleado = db.query(schemas.Empleado).filter(schemas.Empleado.cedula == empleado.cedula).first()
    if db_empleado:
      raise HTTPException(404, "El empleado ya existe")

    del db_empleado

    nuevo_empleado = schemas.Empleado(**empleado.dict())      # creamos al nuevo empleado
    db.add(nuevo_empleado)                                    # lo agregamos a la bd
    db.commit()                                               # confirmamos la inserción
    db.refresh(nuevo_empleado)                                # refrescamos los valores en la variable

    return {"estado": "exitoso", "empleado": nuevo_empleado}  # retornamos al nuevo empleado
  except Exception as e:
    raise HTTPException(400, str(e))


@app.post("/nuevo/promotor")
def crear_promotor(promotor: model.Promotor = Body(...), db: Session = Depends(obtener_bd)):
  try:
    db_promotor = db.query(schemas.Promotor).filter(schemas.Promotor.codigo == promotor.codigo).first()
    if db_promotor:
      raise HTTPException(404, "El promotor ya existe")

    del db_promotor

    nuevo_promotor = schemas.Promotor(**promotor.dict())  # creamos al nuevo promotor
    db.add(nuevo_promotor)                                # mismo que función anterior
    db.commit()
    db.refresh(nuevo_promotor)

    return {"estado": "exitoso", "promotor": nuevo_promotor}
  except Exception as e:
    raise HTTPException(400, str(e))


# noinspection PyTypeChecker
@app.patch("/modificar/empleado/{empleado_id}")
def modificar_empleado(empleado_id: int, empleado: model.Empleado = Body(...), db: Session = Depends(obtener_bd)):
  try:
    consulta_empleado = db.query(schemas.Empleado).filter(schemas.Empleado.cedula == empleado_id)
    db_empleado = consulta_empleado.first()

    if not db_empleado:
      raise HTTPException(404, "Empleado no encontrado")

    empleado.cedula = db_empleado.cedula
    actualizar = empleado.dict(exclude_unset=True)
    consulta_empleado.filter(schemas.Empleado.cedula == empleado_id).update(actualizar, synchronize_session=False)
    db.commit()
    db.refresh(db_empleado)

    return {"estado": "exitoso", "empleado": db_empleado}
  except Exception as e:
    raise HTTPException(400, str(e))

# Asignaciones


@app.post("/asignar/tarea")
def asignar_tarea(tarea_asignar: model.EmpleadoTarea = Body(...), db: Session = Depends(obtener_bd)):
  try:
    empleado = db.query(schemas.Empleado).filter(schemas.Empleado.cedula == tarea_asignar.cedula_empleado).first()
    tarea = db.query(schemas.Tarea).filter(schemas.Tarea.codigo == tarea_asignar.codigo_tareas).first()
    if not empleado and not tarea:
      raise HTTPException(404, "La tarea y el empleado no existen")
    elif not empleado:
      raise HTTPException(404, "El empleado no existe")
    elif not tarea:
      raise HTTPException(404, "La tarea no existe")

    del empleado, tarea

    empleado_asignado = schemas.EmpleadoTarea(**tarea_asignar.dict())  # creamos al nuevo promotor
    db.add(empleado_asignado)  # mismo que función anterior
    db.commit()

    asignacion = db.query(schemas.Tarea, schemas.Empleado) \
      .join(schemas.EmpleadoTarea, schemas.Empleado.cedula == schemas.EmpleadoTarea.cedula_empleado
            and schemas.Tarea.codigo == schemas.EmpleadoTarea.codigo_tareas) \
      .filter(schemas.EmpleadoTarea.id == empleado_asignado.id).all()

    return {"estado": "exitoso", "asignacion": asignacion}
  except Exception as e:
    raise HTTPException(400, str(e))


@app.post("/asignar/proyecto")
def asignar_proyecto(proyecto_asignar: model.EmpleadoProyecto = Body(...), db: Session = Depends(obtener_bd)):
  try:
    empleado = db.query(schemas.Empleado).filter(schemas.Empleado.cedula == proyecto_asignar.cedula_empleado).first()
    proyecto = db.query(schemas.Proyecto).filter(schemas.Proyecto.codigo == proyecto_asignar.codigo_proyecto).first()
    if not empleado and not proyecto:
      raise HTTPException(404, "El proyecto y el empleado no existen")
    elif not empleado:
      raise HTTPException(404, "El empleado no existe")
    elif not proyecto:
      raise HTTPException(404, "El proyecto no existe")

    del empleado, proyecto

    empleado_asignado = schemas.EmpleadoProyecto(**proyecto_asignar.dict())  # creamos al nuevo promotor
    db.add(empleado_asignado)  # mismo que función anterior
    db.commit()

    asignacion = db.query(schemas.Proyecto, schemas.Empleado)\
      .join(schemas.EmpleadoProyecto, schemas.Empleado.cedula == schemas.EmpleadoProyecto.cedula_empleado
            and schemas.Proyecto.codigo == schemas.EmpleadoProyecto.codigo_proyecto)\
      .filter(schemas.EmpleadoProyecto.id == empleado_asignado.id).all()

    return {"estado": "exitoso", "asignacion": asignacion}
  except Exception as e:
    raise HTTPException(400, str(e))


@app.get("/login/{nombre_de_usuario}/{password}")
def login(nombre_de_usuario: str, password: str, db: Session = Depends(obtener_bd)):
  try:
    db_usuario = db.query(schemas.Usuario).filter(schemas.Usuario.usuario == nombre_de_usuario
                                                  and schemas.Usuario.password == password).first()

    if not db_usuario:
      return {"confirmado": "no"}

    if db_usuario.administrador is True:
      return {"confirmado": "si", "administrador": "si"}

    return {"confirmado": "si", "administrador": "no"}
  except Exception as e:
    raise HTTPException(500, str(e))
