# Database
import schemas
from database import SesionLocal, engine, Base
import model

# FastAPI
from fastapi import FastAPI, Depends, Request, Body
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
  DELETE = Borrar

  ¿Y qué son estos? son los métodos de HTTP, recomiendo que lean más acerca de ellos
"""

# TODO: continuar el crud de empleado
# TODO DONE 11/1/2023: login, crear_empleado, crear_promotors

# Abrimos la conexion con la base de datos

db: Session


def obtener_bd():
  global db
  try:
    db = SesionLocal()
    return db
  finally:
    db.close()

# Operaciones de proyectos


@app.get("/proyectos")
def mostrar_proyectos(request: Request, db: Session = Depends(obtener_bd)):
  return {"proyectos": "Not finished"}


@app.post("/crear/proyecto")
def nuevo_proyecto(proyecto: model.Proyectos = Body(...), db: Session = Depends(obtener_bd)):
  # crea un proyecto
  return {"proyectos": "Not finished"}


@app.patch("/modificar/proyecto")
def modificar_proyecto(db: Session = Depends(obtener_bd)):
  # modifica un proyecto
  return {"proyectos": "Not finished"}


@app.delete("/borrar/proyecto")
def borrar_proyecto(db: Session = Depends(obtener_bd)):
  # borra un proyecto
  return {"proyectos": "Not finished"}


@app.get("/proyecto/{proyectoId}")
def mostrar_proyecto(db: Session = Depends(obtener_bd)):
  # TODO: mostrar cada proyecto
  return {"proyectos": "Not finished"}


# Operaciones de tareas

@app.get("/tareas")
def mostrar_tareas(db: Session = Depends(obtener_bd)):
  # muestra las tareas
  return


@app.post("/crear/tarea")
def nueva_tarea(tarea: model.Tareas = Body(...), db: Session = Depends(obtener_bd)):
  # crea una tarea
  return


@app.patch("/modificar/tarea")
def modificar_tarea(db: Session = Depends(obtener_bd)):
  # modifica una tarea
  return


@app.delete("/borrar/tarea")
def borrar_tarea(db: Session = Depends(obtener_bd)):
  # borra una tarea
  return


@app.get("/tarea/{tareaId}")
def mostrar_tarea(db: Session = Depends(obtener_bd)):
  # muestra una tarea
  return


# Operaciones de documentos asociados a cierta tarea

@app.get("/tarea/{tareaId}/documentos")
def docs_tarea(db: Session = Depends(obtener_bd)):
  # muestra las distintas versiones de los documentos de una tarea
  return


@app.post("/tarea/{tareaId}/crear/documento")
def crear_doc(db: Session = Depends(obtener_bd)):
  # crea un documento
  return


# Operaciones de usuario

@app.get("/empleados")
def obtener_empleados(db: Session = Depends(obtener_bd)):
  # obtiene un empleado
  return


@app.get("/empleado/{empleadoId}")
def obtener_empleado(db: Session = Depends(obtener_bd)):
  # obtiene un empleado
  return


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
def crear_promotor(request: Request, promotor: model.Promotor = Body(...), db: Session = Depends(obtener_bd)):
  try:
    nuevo_promotor = schemas.Promotor(**promotor.dict())  # creamos al nuevo promotor
    db.add(nuevo_promotor)                                # mismo que función anterior
    db.commit()
    db.refresh(nuevo_promotor)

    return {"estado": "exitoso", "promotor": nuevo_promotor}
  except Exception as e:
    raise HTTPException(400, str(e))


@app.post("/login")
def login_post(request: Request, usuario: model.PromotorLogin, db: Session = Depends(obtener_bd)):
  try:  # este bloque de código ejecuta to do lo que se encuentre dentro
    promotores = db.query(schemas.Promotor).all()  # obtenemos los promotores
    for promotor in promotores:  # iteramos los promotores

      # lo que está dentro de filter, es literalmente esta sentencia: WHERE usuario = "usuario" AND contra = "contra"
      usuario_login = db.query(schemas.Promotor).filter(usuario.usuario == promotor.usuario and
                                                        usuario.contra == promotor.contra).first()
    if usuario_login is None: # si no conseguimos al usuario
      return {"confirmado": "no"}  # no estara confirmado
    else:  # de lo contrario
      return {"confirmado": "si"}  # estará confirmado
  except Exception as e:  # si al ejecutar algo sucede un error o excepcion, se ejecutara esto
    raise HTTPException(400, str(e))


@app.get("/empleado/{empleadoId}/detalles")
def empleado_detalles(db: Session = Depends(obtener_bd)):
  # mostrar detalles del empleado
  return


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
  # asigna un empleado a un proyecto
  return


@app.post("/asignar/{empleadoId}/{tareaId}")
def asignar_tarea(tarea_asignar: model.EmpleadoTareas = Body(...), db: Session = Depends(obtener_bd)):
  # asigna un empleado a una tarea
  return
