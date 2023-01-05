# Database
from database import SessionLocal, engine
import model

#FastAPI
from fastapi import FastAPI, Depends, Request, Body
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# SQLAlchemy
from sqlalchemy.orm import Session

app = FastAPI()

model.Base.metadata.create_all(bind=engine)

# Abrimos la conexion con la base de datos
def get_database_session():
  try:
    db = SessionLocal()
    yield db
  finally:
    db.close()
  
# Archivos estaticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Archivos HTML
templates = Jinja2Templates(directory="templates")

# Ruta principal del programa
@app.get("/", response_class=HTMLResponse)
def inicio(request: Request):
  # retornamos una página como respuesta
  return templates.TemplateResponse("index.html", {"request": request})

# CRUD de proyectos

@app.get("/proyectos",response_class=HTMLResponse)
def mostrar_proyectos(request: Request, db: Session = Depends(get_database_session)):
  # recibimos una instancia de la clase Test con los datos de la base de datos y lo retornamos
  mensaje = db.query(model.Test.message).first() # message = Hello world!
  
  # TODO: realizar SSR de los proyectos, cabe destacar que deben estar en una linked list
  return templates.TemplateResponse("proyectos.html", {"request": request, "message": mensaje[0]})

@app.post("/crear/proyecto")
def nuevo_proyecto(proyecto: model.Proyectos = Body(...)):
  # crea un proyecto
  return

@app.put("/modificar/proyecto")
def modificar_proyecto():
  # modifica un proyecto
  return

@app.delete("/borrar/proyecto")
def borrar_proyecto():
  # borra un proyecto
  return

@app.get("/proyecto/{proyectoId}", response_class=HTMLResponse)
def mostrar_proyecto():
  # TODO: mostrar cada proyecto
  return

# Operaciones de tareas

@app.get("/tareas", response_class=HTMLResponse)
def mostrar_tareas():
  # muestra las tareas
  return

@app.post("/crear/tarea")
def nueva_tarea(tarea: model.Tareas = Body(...)):
  # crea una tarea
  return

@app.put("/modificar/tarea")
def modificar_tarea():
  # modifica una tarea
  return

@app.delete("/borrar/tarea")
def borrar_tarea():
  # borra una tarea
  return

@app.get("/tarea/{tareaId}", response_class=HTMLResponse)
def mostrar_tarea():
  # muestra cada tarea
  return

# Operaciones de documentos asociados a cierta tarea

@app.get("/tarea/{tareaId}/documentos", response_class=HTMLResponse)
def docs_tarea():
  # muestra las distintas versiones de los documentos de una tarea
  return

@app.post("/tarea/{tareaId}/crear/documento")
def crear_doc():
  # crea un documento
  return

# Operaciones de usuario

@app.get("/signup", response_class=HTMLResponse)
def crear_cuenta():
  # crea una cuenta
  return

@app.post("/signup")
def crear_cuenta_post(request: Request, empleado: model.Empleado = Body(...)):
  # verifica los datos y los envia
  return

@app.get("/login",response_class=HTMLResponse)
def login_get(request: Request):
  # Muestra el HTML para iniciar sesión
  return

@app.post("/login",response_class=HTMLResponse)
def login_post(request: Request):
  # Recibe los datos del formulario y valida los datos
  return

@app.get("/dashboard/{usuarioId}", response_class=HTMLResponse)
def panel(request: Request):
  # muestra el dashboard con proyectos y tareas a los que se pueden adscribir los clientes
  return

@app.get("/user/{usuarioId}/detalles", response_class=HTMLResponse)
def mostrar_usuario():
  # mostrar detalles del usuario
  return

@app.put("/modificar/usuario")
def modificar_usuario():
  # modifica datos del usuario
  return

@app.delete("/borrar/usuario")
def borrar_usuario():
  # modifica datos del usuario
  return

@app.post("/asignar/{usuarioId}/{proyectoId}")
def asignar_proyecto(proyecto_asignar: model.EmpleadoProyecto = Body(...)):
  # asigna un usuario a un proyecto
  return

@app.post("/asignar/{usuarioId}/{tareaId}")
def asignar_tarea(tarea_asignar: model.EmpleadoTareas = Body(...)):
  # asigna un usuario a una tarea
  return