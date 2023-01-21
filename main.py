# Database
import schemas
from database import SesionLocal, engine, Base
from estructuras import Lista, Pila
import model

# FastAPI
from fastapi import FastAPI, Depends, Body
from fastapi.exceptions import HTTPException
# SQLAlchemy
from sqlalchemy.orm import Session
from sqlalchemy import select

app = FastAPI()

Base.metadata.create_all(bind=engine)

"""
  ¿Qué es GET, POST, patch Y DELETE?

  GET = Obtener
  POST = Crear
  PATCH = Actualizar parcialmente
  patch = actualizar algo completamente
  DELETE = Borrar

  ¿Y qué son estos? son los métodos de HTTP, recomiendo que lean más acerca de ellos
"""

# TODO: CREAR NUEVAS RUTAS (Luis)
# TODO: ELIMINA RUTAS ASOCIADAS A LOS DOCUMENTOS DE UNA TAREA
# TODO: "/proyecto/{proyecto_id}/empleados/" EMPLEADOS DE UN PROYECTO
# TODO: "/tarea/{tarea_id}/empleados/" EMPLEADOS DE UNA TAREA
# TODO: "/proyecto/{proyecto_id/}/tareas" TAREAS DE UN PROYECTO
# TODO: "/proyecto/{proyecto_id/crear/tarea/" CREAR UNA TAREA ASOCIADA A CIERTO PROYECTO
# TODO: "/proyecto/{proyecto_id/tarea/{tarea_id}" RUTA GET, patch Y DELETE DE UNA TAREA
# TODO: "/proyecto/{proyecto_id/tarea/{tarea_id}/docs" RUTA GET, POST, patch Y DELETE DE UN DOCUMENTO ASOCIADO A UNA TAREA
# TODO DONE 11/1/2023: login, crear_empleado, crear_promotor
# TODO DONE 12/1/2023: terminadas rutas POST simples :D
# TODO DONE 13/1/2023: adelantadas rutas de asignacion de proyectos y tareas
# TODO DONE 14/1/2023: añadidas algunas funciones GET
# TODO DONE 15/1/2023: añadido uso de estructuras de datos y GET de varios registros :3

# Abrimos la conexion con la base de datos

connection: Session


def obtener_bd():
  global connection
  try:
    connection = SesionLocal()
    return connection
  finally:
    connection.close()

# Operaciones de proyectos


@app.get("/")
def home():
  return {"estructura de la API": {  # no hacer caso a esto
      "/proyectos": {
        "descripcion": "muestra todos los proyectos",
        "metodo": "GET",
        "terminado": "si"
      },
      "/crear/proyecto": {
        "descripcion": "crea un nuevo proyecto",
        "metodo": "POST",
        "terminado": "si"
      },
      "/modificar/proyecto/{proyecto_id}": {
        "descripcion": "actualiza un proyecto existente",
        "metodo": "patch",
        "terminado": "no"
      },
      "/borrar/proyecto/{proyecto_id}": {
        "descripcion": "borra un proyecto existente",
        "metodo": "DELETE",
        "terminado": "no"
      },
      "/proyecto/{proyecto_id}": {
        "descripcion": "muestra un proyecto existente",
        "metodo": "GET",
        "terminado": "si"
      },
      "/tareas": {
        "descripcion": "muestra todas las tareas",
        "metodo": "GET",
        "terminado": "si"
      },
      "/crear/tarea": {
        "descripcion": "crea una nueva tarea",
        "metodo": "POST",
        "terminado": "si"
      },
      "/modificar/tarea/{tarea_id}": {
        "descripcion": "actualiza una tarea existente",
        "metodo": "patch",
        "terminado": "no"
      },
      "/borrar/tarea/{tarea_id}": {
        "descripcion": "borra una tarea",
        "metodo": "DELETE",
        "terminado": "no"
      },
      "/tarea/{tarea_id}": {
        "descripcion": "muestra una tarea",
        "metodo": "GET",
        "terminado": "si"
      },
      "/tareas/{tarea_id}/documentos": {
        "descripcion": "muestra los documentos asociados a cada tarea",
        "metodo": "GET",
        "terminado": "no"
      },
      "/tareas/{tarea_id}/crear/documento": {
        "descripcion": "muestra los documentos asociados a cada tarea",
        "metodo": "POST",
        "terminado": "si"
      },
      "/tareas/{tarea_id}/modificar/documento/{documento_id}": {
        "descripcion": "actualiza un documento",
        "metodo": "patch",
        "terminado": "no"
      },
      "/empleados": {
        "descripcion": "muestra todos los empleados",
        "metodo": "GET",
        "terminado": "si"
      },
      "/empleado/{empleado_id}": {
        "descripcion": "muestra un empleados",
        "metodo": "GET",
        "terminado": "si"
      },
      "/crear/empleado": {
        "descripcion": "crea un empleado",
        "metodo": "POST",
        "terminado": "si"
      },
      "/crear/promotor": {
        "descripcion": "crea un promotor",
        "metodo": "POST",
        "terminado": "si"
      },
      "/modificar/empleado/{empleado_id}": {
        "descripcion": "modifica un empleado",
        "metodo": "patch",
        "terminado": "no"
      },
      "/borrar/empleado/{empleado_id}": {
        "descripcion": "elimina un empleado",
        "metodo": "DELETE",
        "terminado": "no"
      },
      "/asignar/proyecto/{empleado_id}/{proyecto_id}": {
        "descripcion": "asigna un empleado a un proyecto",
        "metodo": "POST",
        "terminado": "si"
      },
      "/asignar/tarea/{empleado_id}/{tarea_id}": {
        "descripcion": "asigna un empleado a una tarea",
        "metodo": "POST",
        "terminado": "si"
      },
   }
  }


@app.get("/proyectos")
def mostrar_proyectos(db: Session = Depends(obtener_bd)):
  try:
    # definimos una lista
    proyectos_lista = Lista()

    # obtenemos los datos de la bd: SELECT * FROM proyectos
    proyectos = db.query(schemas.Proyectos).all()

    for proyecto in proyectos:  # iteramos el objeto
      proyectos_lista.agregar_final(proyecto.nombre)  # empujamos por atrás el nombre

    respuesta = proyectos_lista.retornar_datos()  # retornamos los datos de la lista

    del proyectos_lista  # borramos la variable para liberar memoria

    return {"cantidad": len(respuesta), "proyectos": respuesta}
  except Exception as e:
    raise HTTPException(400, str(e))


@app.post("/crear/proyecto")
def agregar_proyecto(proyecto: model.Proyectos = Body(...), db: Session = Depends(obtener_bd)):
  try:
    nuevo_proyecto = schemas.Proyectos(**proyecto.dict())     # creamos al nuevo proyecto
    db.add(nuevo_proyecto)                                    # lo agregamos a la bd
    db.commit()                                               # confirmamos la inserción
    db.refresh(nuevo_proyecto)                                # refrescamos los valores en la variable

    return {"estado": "exitoso", "empleado": nuevo_proyecto}  # retornamos al nuevo proyecto
  except Exception as e:
    raise HTTPException(400, str(e))


@app.patch("/modificar/proyecto/{proyecto_id}")
def actualizar_proyecto(proyecto_id: int, proyecto: model.Proyectos = Body(...), db: Session = Depends(obtener_bd)):
  try:
    consulta_proyecto = db.query(schemas.Proyectos).filter(schemas.Proyectos.codigo == proyecto_id)
    db_proyecto = consulta_proyecto.first()

    if not db_proyecto: raise HTTPException(404, "Proyecto no encontrado")

    actualizar = proyecto.dict(exclude_unset=True)
    consulta_proyecto.filter(schemas.Proyectos.codigo == proyecto_id).update(actualizar, synchronize_session=False)
    db.commit()
    db.refresh(db_proyecto)

    return {"estado": "exitoso", "proyecto": db_proyecto}
  except Exception as e:
    raise HTTPException(400, str(e))


@app.delete("/borrar/proyecto/{proyecto_id}")
def borrar_proyecto(proyecto_id: int, db: Session = Depends(obtener_bd)):
  try:
    consulta_proyecto = db.query(schemas.Proyectos).filter(schemas.Proyectos.codigo == proyecto_id)
    proyecto = consulta_proyecto.first()
    if not proyecto: raise HTTPException(404, "No existe el empleado")

    consulta_proyecto.delete(synchronize_session=False)
    db.commit()
    return {"estado": "exitoso"}
  except Exception as e:
    raise HTTPException(400, str(e))


@app.get("/proyecto/{proyecto_id}")
def mostrar_proyecto(proyecto_id: int, db: Session = Depends(obtener_bd)):
  try:
    proyecto = db.query(schemas.Proyectos).get(proyecto_id)  # SELECT * FROM proyectos WHERE codigo = proyecto_id

    if proyecto is None:
      return {"detail": "El producto no existe"}

    return {"proyecto": proyecto}  # retornamos el proyecto
  except Exception as e:
    raise HTTPException(400, str(e))

# Operaciones de tareas


@app.get("/proyecto/{proyecto_id}/empleados")
def empleados_del_proyecto(proyecto_id: int, db: Session = Depends(obtener_bd)):
  try:
    empleados_pila = Pila()
    empleados_proyecto = db.query(schemas.Empleado)\
      .join(schemas.EmpleadoProyectos, schemas.Empleado.cedula == schemas.EmpleadoProyectos.cedula_empleado
            and proyecto_id == schemas.EmpleadoProyectos.codigo_proyecto).all()

    for empleado in empleados_proyecto:
      empleados_pila.apilar(f"{empleado.nombre} {empleado.apellido}")

    respuesta = empleados_pila.retornar_datos()

    return {"cantidad": len(respuesta), "tareas": respuesta}
  except Exception as e:
    raise HTTPException(400, str(e))


@app.get("/proyecto/{proyecto_id}/tareas")
def mostrar_tareas(proyecto_id: int, db: Session = Depends(obtener_bd)):
  try:
    tareas_lista = Lista()
    tareas = db.query(schemas.Tareas).filter(schemas.Tareas.codigo_proyecto == proyecto_id)

    for tarea in tareas:
      tareas_lista.agregar_final(tarea)

    respuesta = tareas_lista.retornar_datos()

    return {"cantidad": len(respuesta), "tareas": respuesta}
  except Exception as e:
    raise HTTPException(400, str(e))


@app.post("/crear/tarea")
def agregar_tarea(proyecto_id: int, tarea: model.Tareas = Body(...), db: Session = Depends(obtener_bd)):
  try:
    tarea.codigo_proyecto = proyecto_id
    nueva_tarea = schemas.Tareas(**tarea.dict())        # creamos a la nueva tarea
    db.add(nueva_tarea)                                 # lo agregamos a la bd
    db.commit()                                         # confirmamos la inserción
    db.refresh(nueva_tarea)                             # refrescamos los valores en la variable
    return {"estado": "exitoso", "tarea": nueva_tarea}  # retornamos al nuevo empleado
  except Exception as e:
    raise HTTPException(400, str(e))


@app.patch("/tarea/{tarea_id}")
def modificar_tarea(tarea_id: int, tarea: schemas.Tareas = Body(...), db: Session = Depends(obtener_bd)):
  try:
    consulta_tarea = db.query(schemas.Tareas).filter(schemas.Tareas.codigo == tarea_id)
    db_tarea = consulta_tarea.first()

    if not db_tarea: raise HTTPException(404, "Tarea no encontrada")

    actualizar = tarea.dict(exclude_unset=True)
    consulta_tarea.filter(schemas.Tareas.codigo == tarea_id).update(actualizar, synchronize_session=False)
    db.commit()
    db.refresh(db_tarea)

    return {"estado": "exitoso", "proyecto": db_tarea}
  except Exception as e:
    raise HTTPException(400, str(e))
  return


@app.delete("/tarea/{tarea_id}")
def borrar_tarea(tarea_id: int, db: Session = Depends(obtener_bd)):
  try:
    consulta_tarea = db.query(schemas.Tareas).filter(schemas.Tareas.codigo == tarea_id)
    tarea = consulta_tarea.first()
    if not tarea: raise HTTPException(404, "No existe la tarea")

    consulta_tarea.delete(synchronize_session=False)
    db.commit()
    return {"estado": "exitoso"}
  except Exception as e:
    raise HTTPException(400, str(e))


@app.get("/proyecto/{proyecto_id}/tarea/{tarea_id}")
def mostrar_tarea(proyecto_id: int, tarea_id: int, db: Session = Depends(obtener_bd)):
  try:
    tarea = db.query(schemas.Tareas).filter(schemas.Proyectos.codigo == proyecto_id).get(tarea_id)

    if tarea is None:
      return {"detail": "La tarea no existe"}

    return {"tarea": tarea}
  except Exception as e:
    raise HTTPException(400, str(e))


@app.get("/tarea/{tarea_id}/empleados")
def empleados_del_proyecto(tarea_id: int, db: Session = Depends(obtener_bd)):
  try:
    empleados_pila = Pila()
    empleados_tarea = db.query(schemas.Empleado)\
      .join(schemas.EmpleadoTareas, schemas.Empleado.cedula == schemas.EmpleadoTareas.cedula_empleado
            and schemas.Tareas.codigo == schemas.EmpleadoTareas.codigo_tarea)\
      .filter(schemas.EmpleadoTareas.codigo_tarea == tarea_id).all()

    for empleado in empleados_tarea:
      empleados_pila.apilar(f"{empleado.nombre} {empleado.apellido}")

    respuesta = empleados_pila.retornar_datos()

    return {"cantidad": len(respuesta), "tareas": respuesta}
  except Exception as e:
    raise HTTPException(400, str(e))

# Operaciones de documentos asociados a cierta tarea

@app.get("/tarea/{tarea_id}/docs")
def docs_tarea(db: Session = Depends(obtener_bd)):
  try:
    docs_pila = Pila()  # creamos una pila
    documentos = db.query(schemas.Documentos).all()  # obtenemos todos los registros de empleado

    for documento in documentos:  # iteramos el objeto
      # apilamos el nombre y el apellido
      docs_pila.apilar(f"{documento.nombre.title()} {documento.apellido.title()}")

    respuesta = docs_pila.retornar_datos()

    return {"cantidad": len(respuesta), "empleados": respuesta}
  except Exception as e:
    raise HTTPException(400, str(e))


@app.post("/proyecto/{proyecto_id}/tarea/{tarea_id}/docs")
def crear_doc(proyecto_id: int, tarea_id: int, documento: model.Documentos, db: Session = Depends(obtener_bd)):
  try:
    documento.codigo_tarea = tarea_id
    nuevo_doc = schemas.Empleado(**documento.dict())      # creamos al nuevo documento
    db.add(nuevo_doc)                                     # lo agregamos a la bd
    db.commit()                                           # confirmamos la inserción
    db.refresh(nuevo_doc)                                 # refrescamos los valores en la variable

    version = model.Version()
    version.codigo_documentos = documento.codigo
    version.descripcion = documento.descripcion
    version.codigo = documento.codigo
    nueva_version = schemas.Version(**version.dict())
    db.add(nueva_version)
    db.commit()
    db.refresh(nuevo_doc)

    return {"estado": "exitoso", "documento": nuevo_doc, "version": nueva_version}  # retornamos al nuevo documento
  except Exception as e:
    raise HTTPException(400, str(e))


@app.get("/empleados")
def obtener_empleados(db: Session = Depends(obtener_bd)):
  try:
    empleados_pila = Pila()  # creamos una pila
    empleados = db.query(schemas.Empleado).all()  # obtenemos todos los registros de empleado

    for empleado in empleados:  # iteramos el objeto
      # apilamos el nombre y el apellido
      empleados_pila.apilar(f"{empleado.nombre.title()} {empleado.apellido.title()}")

    respuesta = empleados_pila.retornar_datos()

    return {"cantidad": len(respuesta), "empleados": respuesta}
  except Exception as e:
    raise HTTPException(400, str(e))


@app.get("/empleado/{empleado_id}")
def obtener_empleado(empleado_id: int, db: Session = Depends(obtener_bd)):
  try:
    empleado = db.query(schemas.Empleado).get(empleado_id)  # SELECT * FROM empleado WHERE cedula = empleado_id

    if empleado is None:
      return {"detail": "El empleado no existe"}

    return {"empleado": empleado}
  except Exception as e:
    raise HTTPException(400, str(e))


@app.post("/nuevo/empleado")
def crear_empleado(empleado: model.Empleado = Body(...), db: Session = Depends(obtener_bd)):
  try:
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
    nuevo_promotor = schemas.Promotor(**promotor.dict())  # creamos al nuevo promotor
    db.add(nuevo_promotor)                                # mismo que función anterior
    db.commit()
    db.refresh(nuevo_promotor)

    return {"estado": "exitoso", "promotor": nuevo_promotor}
  except Exception as e:
    raise HTTPException(400, str(e))


@app.post("/login")
def login_post(usuario: model.PromotorLogin, db: Session = Depends(obtener_bd)):
  try:                                                      # ejecuta to do lo que se encuentre dentro si no hay errores
    promotores = db.query(schemas.Promotor).all()           # obtenemos los promotores
    for promotor in promotores:                             # iteramos los promotores

      usuario_login = db.query(schemas.Promotor)\
        .filter(usuario.usuario == promotor.usuario         # filter = WHERE usuario = "usuario" AND contra = "contra"
                and usuario.contra == promotor.contra)\
        .first()                                            # arrojamos la primera coincidencia

    if usuario_login is None:                               # si no conseguimos al usuario
      return {"confirmado": "no"}                           # no estará confirmado
    else:  # de lo contrario
      return {"confirmado": "si"}                           # estará confirmado
  except Exception as e:                                    # si sucede un error o excepción, se ejecutará esto
    raise HTTPException(400, str(e))


@app.patch("/modificar/empleado/{empleado_id}")
def modificar_empleado(empleado_id: int, empleado: model.Empleado = Body(...), db: Session = Depends(obtener_bd)):
  try:
    consulta_empleado = db.query(schemas.Empleado).filter(schemas.Empleado.cedula == empleado_id)
    db_empleado = consulta_empleado.first()

    if not db_empleado: raise HTTPException(404, "Empleado no encontrado")

    actualizar = empleado.dict(exclude_unset=True)
    consulta_empleado.filter(schemas.Empleado.cedula == empleado_id).update(actualizar, synchronize_session=False)
    db.commit()
    db.refresh(db_empleado)

    return {"estado": "exitoso", "proyecto": db_empleado}
  except Exception as e:
    raise HTTPException(400, str(e))


@app.delete("/borrar/empleado/{empleado_id}")
def borrar_empleado(empleado_id: int, db: Session = Depends(obtener_bd)):
  try:
    consulta_empleado = db.query(schemas.Empleado).filter(schemas.Empleado == empleado_id)
    empleado = consulta_empleado.first()
    if not empleado: raise HTTPException(404, "No existe el empleado")

    consulta_empleado.delete(synchronize_session=False)
    db.commit()
    return {"estado": "exitoso"}
  except Exception as e:
    raise HTTPException(400, str(e))

# Asignaciones


@app.post("/asignar/tarea")
def asignar_proyecto(tarea_asignar: model.EmpleadoTareas = Body(...), db: Session = Depends(obtener_bd)):
  try:
    empleado_asignado = schemas.EmpleadoTareas(**tarea_asignar.dict())  # creamos al nuevo promotor
    db.add(empleado_asignado)  # mismo que función anterior
    db.commit()

    asignacion = db.query(schemas.Tareas, schemas.Empleado) \
      .join(schemas.EmpleadoTareas, schemas.Empleado.cedula == schemas.EmpleadoTareas.cedula_empleado
            and schemas.Tareas.codigo == schemas.EmpleadoTareas.codigo_tarea) \
      .filter(schemas.EmpleadoTareas.id == empleado_asignado.id).all()

    return {"estado": "exitoso", "asignacion": asignacion}
  except Exception as e:
    raise HTTPException(400, str(e))


@app.post("/asignar/proyecto")
def asignar_tarea(proyecto_asignar: model.EmpleadoProyecto = Body(...), db: Session = Depends(obtener_bd)):
  try:
    empleado_asignado = schemas.EmpleadoProyectos(**proyecto_asignar.dict())  # creamos al nuevo promotor
    db.add(empleado_asignado)  # mismo que función anterior
    db.commit()

    asignacion = db.query(schemas.Proyectos, schemas.Empleado)\
      .join(schemas.EmpleadoProyectos, schemas.Empleado.cedula == schemas.EmpleadoProyectos.cedula_empleado
            and schemas.Proyectos.codigo == schemas.EmpleadoProyectos.codigo_proyecto)\
      .filter(schemas.EmpleadoProyectos.id == empleado_asignado.id).all()

    return {"estado": "exitoso", "asignacion": asignacion}
  except Exception as e:
    raise HTTPException(400, str(e))
