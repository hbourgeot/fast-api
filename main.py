# Database
from database import SessionLocal, engine
import model

# FastAPI
from fastapi import FastAPI, Depends, Request, Body
from fastapi.responses import HTMLResponse

# SQLAlchemy
from sqlalchemy.orm import Session

app = FastAPI()

model.Base.metadata.create_all(bind=engine)

# Abrimos la conexion con la base de datos


def obtener_bd():
  try:
    db = SessionLocal()
    return db
  finally:
    db.close()


# Ruta principal del programa
@app.get("/", response_class=HTMLResponse)
def inicio(request: Request):
  # retornamos una página como respuesta
  return {"hello world": "Hola mundo!"}

# CRUD de proyectos

@app.get("/proyectos",response_class=HTMLResponse)
def mostrar_proyectos(request: Request, db: Session = Depends(obtener_bd)):
  return {"proyectos": "Not finished"}

@app.post("/crear/proyecto")
def nuevo_proyecto(proyecto: model.Proyectos = Body(...), db: Session = Depends(obtener_bd)):
  # crea un proyecto
  return {"proyectos": "Not finished"}

@app.put("/modificar/proyecto")
def modificar_proyecto(db: Session = Depends(obtener_bd)):
  # modifica un proyecto
  return {"proyectos": "Not finished"}

@app.delete("/borrar/proyecto")
def borrar_proyecto(db: Session = Depends(obtener_bd)):
  # borra un proyecto
  return {"proyectos": "Not finished"}

@app.get("/proyecto/{proyectoId}", response_class=HTMLResponse)
def mostrar_proyecto(db: Session = Depends(obtener_bd)):
  # TODO: mostrar cada proyecto
  return {"proyectos": "Not finished"}

# Operaciones de tareas

@app.get("/tareas", response_class=HTMLResponse)
def mostrar_tareas(db: Session = Depends(obtener_bd)):
  # muestra las tareas
  return

@app.post("/crear/tarea")
def nueva_tarea(tarea: model.Tareas = Body(...), db: Session = Depends(obtener_bd)):
  # crea una tarea
  return

@app.put("/modificar/tarea")
def modificar_tarea(db: Session = Depends(obtener_bd)):
  # modifica una tarea
  return

@app.delete("/borrar/tarea")
def borrar_tarea(db: Session = Depends(obtener_bd)):
  # borra una tarea
  return

@app.get("/tarea/{tareaId}", response_class=HTMLResponse)
def mostrar_tarea(db: Session = Depends(obtener_bd)):
  # muestra cada tarea
  return

# Operaciones de documentos asociados a cierta tarea

@app.get("/tarea/{tareaId}/documentos", response_class=HTMLResponse)
def docs_tarea(db: Session = Depends(obtener_bd)):
  # muestra las distintas versiones de los documentos de una tarea
  return

@app.post("/tarea/{tareaId}/crear/documento")
def crear_doc(db: Session = Depends(obtener_bd)):
  # crea un documento
  return

# Operaciones de usuario

@app.get("/signup", response_class=HTMLResponse)
def crear_cuenta(db: Session = Depends(obtener_bd)):
  # crea una cuenta
  return

@app.post("/signup")
def crear_cuenta_post(request: Request, empleado: model.Empleado = Body(...), db: Session = Depends(obtener_bd)):
  # verifica los datos y los envia
  return

@app.get("/login",response_class=HTMLResponse)
def login_get(request: Request, db: Session = Depends(obtener_bd)):
  # Muestra el HTML para iniciar sesión
  return

@app.post("/login",response_class=HTMLResponse)
def login_post(request: Request, db: Session = Depends(obtener_bd)):
  # Recibe los datos del formulario y valida los datos
  return

@app.get("/dashboard/{usuarioId}", response_class=HTMLResponse)
def panel(request: Request, db: Session = Depends(obtener_bd)):
  # muestra el dashboard con proyectos y tareas a los que se pueden adscribir los clientes
  return

@app.get("/user/{usuarioId}/detalles", response_class=HTMLResponse)
def mostrar_usuario(db: Session = Depends(obtener_bd)):
  # mostrar detalles del usuario
  return

@app.put("/modificar/usuario")
def modificar_usuario(db: Session = Depends(obtener_bd)):
  # modifica datos del usuario
  return

@app.delete("/borrar/usuario")
def borrar_usuario(db: Session = Depends(obtener_bd)):
  # modifica datos del usuario
  return

@app.post("/asignar/{usuarioId}/{proyectoId}")
def asignar_proyecto(proyecto_asignar: model.EmpleadoProyecto = Body(...), db: Session = Depends(obtener_bd)):
  # asigna un usuario a un proyecto
  return

@app.post("/asignar/{usuarioId}/{tareaId}")
def asignar_tarea(tarea_asignar: model.EmpleadoTareas = Body(...), db: Session = Depends(obtener_bd)):
  # asigna un usuario a una tarea
  return