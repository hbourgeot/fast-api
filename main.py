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

app = FastAPI()

Base.metadata.create_all(bind=engine)

"""
  ¿Qué es GET, POST, PUT Y DELETE?

  GET = Obtener
  POST = Crear
  PATCH = Actualizar parcialmente
  PUT = actualizar algo completamente
  DELETE = Borrar

  ¿Y qué son estos? son los métodos de HTTP, recomiendo que lean más acerca de ellos
"""

# TODO: continuar el crud de empleado
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


@app.get("/proyectos")
def mostrar_proyectos(db: Session = Depends(obtener_bd)):
  try:
    # definimos una lista
    proyectos_lista = Lista()

    # obtenemos los datos de la bd
    proyectos = db.query(schemas.Proyectos).all()

    for proyecto in proyectos:  # iteramos el objeto
      proyectos_lista.agregar_final(proyecto.nombre)  # empujamos por atrás el nombre

    respuesta = proyectos_lista.retornar_datos()  # retornamos los datos de la lista

    return {"cantidad":len(respuesta),"proyectos":respuesta}
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


@app.put("/modificar/proyecto/{proyecto_id}")
def actualizar_proyecto(db: Session = Depends(obtener_bd)):
  # modifica un proyecto
  return {"proyectos": "Not finished"}


@app.patch("/modificar/proyecto/{proyecto_id}")
def modificar_proyecto(db: Session = Depends(obtener_bd)):
  # modifica un proyecto
  return {"proyectos": "Not finished"}


@app.delete("/borrar/proyecto/{proyecto_id}")
def borrar_proyecto(db: Session = Depends(obtener_bd)):
  # borra un proyecto
  return {"proyectos": "Not finished"}


@app.get("/proyecto/{proyecto_id}")
def mostrar_proyecto(proyecto_id: str, db: Session = Depends(obtener_bd)):
  try:
    proyecto = db.query(schemas.Proyectos).get(proyecto_id)  # SELECT * FROM proyectos WHERE codigo = proyecto_id

    if proyecto is None:
      return {"detail": "El producto no existe"}

    return {"proyecto":proyecto}
  except Exception as e:
    raise HTTPException(400,str(e))


# Operaciones de tareas


@app.get("/tareas")
def mostrar_tareas(db: Session = Depends(obtener_bd)):
  try:
    tareas_lista = Lista()
    tareas = db.query(schemas.Tareas).all()

    for tarea in tareas:
      tareas_lista.agregar_final(tarea.descripcion)

    respuesta = tareas_lista.retornar_datos()

    return {"cantidad": len(respuesta), "tareas": respuesta}
  except Exception as e:
    raise HTTPException(400, str(e))


@app.post("/crear/tarea")
def agregar_tarea(tarea: model.Tareas = Body(...), db: Session = Depends(obtener_bd)):
  try:
    nueva_tarea = schemas.Tareas(**tarea.dict())        # creamos a la nueva tarea
    db.add(nueva_tarea)                                 # lo agregamos a la bd
    db.commit()                                         # confirmamos la inserción
    db.refresh(nueva_tarea)                             # refrescamos los valores en la variable

    return {"estado": "exitoso", "tarea": nueva_tarea}  # retornamos al nuevo empleado
  except Exception as e:
    raise HTTPException(400, str(e))


@app.patch("/modificar/tarea")
def modificar_tarea(db: Session = Depends(obtener_bd)):
  # modifica una tarea
  return


@app.delete("/borrar/tarea")
def borrar_tarea(db: Session = Depends(obtener_bd)):
  # borra una tarea
  return


@app.get("/tarea/{tarea_id}")
def mostrar_tarea(tarea_id: int, db: Session = Depends(obtener_bd)):
  try:
    tarea = db.query(schemas.Tareas).get(tarea_id)

    if tarea is None:
      return {"detail": "La rarea no existe"}

    return {"tarea": tarea}
  except Exception as e:
    raise HTTPException(400, str(e))


# Operaciones de documentos asociados a cierta tarea


@app.get("/tarea/{tareaId}/documentos")
def docs_tarea(db: Session = Depends(obtener_bd)):
  # muestra las distintas versiones de los documentos de una tarea
  return


@app.post("/tarea/{tarea_id}/crear/documento")
def crear_doc(tarea_id: int, documento: model.Documentos, db: Session = Depends(obtener_bd)):
  try:
    documento.codigo_tarea = tarea_id
    nuevo_doc = schemas.Empleado(**documento.dict())      # creamos al nuevo documento
    db.add(nuevo_doc)                                     # lo agregamos a la bd
    db.commit()                                           # confirmamos la inserción
    db.refresh(nuevo_doc)                                 # refrescamos los valores en la variable

    return {"estado": "exitoso", "documento": nuevo_doc}  # retornamos al nuevo empleado
  except Exception as e:
    raise HTTPException(400, str(e))


@app.put("/tarea/{tarea_id}/modificar/{documento_id}")
def modificar_documento(db: Session = Depends(obtener_bd)):
  # modifica un documento
  return

# Operaciones de usuario


@app.get("/empleados")
def obtener_empleados(db: Session = Depends(obtener_bd)):
  try:
    empleados_pila = Pila()
    empleados = db.query(schemas.Empleado).all()

    for empleado in empleados:
      empleados_pila.apilar(f"{empleado.nombre.title()} {empleado.apellido.title()}")

    respuesta = empleados_pila.retornar_datos()

    return {"cantidad": len(respuesta), "proyectos": respuesta}
  except Exception as e:
    raise HTTPException(400, str(e))


@app.get("/empleado/{empleado_id}")
def obtener_empleado(empleado_id: int, db: Session = Depends(obtener_bd)):
  try:
    empleado = db.query(schemas.Empleado).get(empleado_id)

    if empleado is None:
      return {"detail": "El producto no existe"}

    return {"empleado":empleado}
  except Exception as e:
    raise HTTPException(400,str(e))


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


@app.patch("/modificar/empleado")
def modificar_empleado(db: Session = Depends(obtener_bd)):
  # modifica datos del empleado
  return


@app.delete("/borrar/empleado")
def borrar_empleado(db: Session = Depends(obtener_bd)):
  # modifica datos del empleado
  return

# Asignaciones


@app.post("/asignar/{empleadoId}/{proyectoId}")
def asignar_proyecto(proyecto_asignar: model.EmpleadoProyecto = Body(...), db: Session = Depends(obtener_bd)):
  respuesta: dict
  try:
    empleado_asignado = schemas.EmpleadoProyectos(**proyecto_asignar.dict())  # creamos al nuevo promotor
    db.add(empleado_asignado)  # mismo que función anterior
    db.commit()

    asignacion_proyecto = db.query(schemas.EmpleadoProyectos)\
      .join(schemas.Empleado).filter(schemas.EmpleadoProyectos.cedula_empleado == schemas.Empleado.cedula)\
      .join(schemas.Proyectos).filter(schemas.EmpleadoProyectos.codigo_proyecto == schemas.Proyectos.codigo)

    for empleado, proyecto in asignacion_proyecto:
      respuesta["proyecto"] += proyecto
      respuesta["empleado"] += empleado

    return {"estado": "exitoso", "asignacion": respuesta}
  except Exception as e:
    raise HTTPException(400, str(e))


@app.post("/asignar/{empleadoId}/{tareaId}")
def asignar_tarea(tarea_asignar: model.EmpleadoTareas = Body(...), db: Session = Depends(obtener_bd)):
  respuesta: dict
  try:
    empleado_asignado = schemas.EmpleadoProyectos(**tarea_asignar.dict())  # creamos al nuevo promotor
    db.add(empleado_asignado)  # mismo que función anterior
    db.commit()

    asignacion_tarea = db.query(schemas.EmpleadoProyectos) \
      .join(schemas.Empleado).filter(schemas.EmpleadoProyectos.cedula_empleado == schemas.Empleado.cedula) \
      .join(schemas.Proyectos).filter(schemas.EmpleadoProyectos.codigo_proyecto == schemas.Proyectos.codigo)

    for empleado, proyecto in asignacion_tarea:
      respuesta["proyecto"] += proyecto
      respuesta["empleado"] += empleado

    return {"estado": "exitoso", "asignacion": respuesta}
  except Exception as e:
    raise HTTPException(400, str(e))
