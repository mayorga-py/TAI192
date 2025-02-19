from fastapi import FastAPI,HTTPException
from typing import Optional

app= FastAPI (
    title= "API de Gestión de Tareas (To-Do List)",
    description= "por Luis Eduardo Mayorga Becerra",
    version="1.2"
)
tareas=[
    {"id":1 ,"titulo":"respaso de TAI 1", "descripcion":"Repasar los apuntes de TAI", "vencimiento":"14-02-24", "Estado":"completada"},
    {"id":2 ,"titulo":"SIIEEQ", "descripcion":"historial de la vida academica de los alumnos", "vencimiento":"18-02-25", "Estado":"completada"},
    {"id":3 ,"titulo":"PREV-OUT", "descripcion":"preveir la baja academica", "vencimiento":"22-02-25", "Estado":"en progreso"},
    {"id":4 ,"titulo":"Enseñame", "descripcion":"inteprete de movimientos", "vencimiento":"31-07-25", "Estado":"en progreso"},
    {"id":5 ,"titulo":"Calfig", "descripcion":"claculadora para fisica", "vencimiento":"14-02-25", "Estado":"completada"},
]

# Obtener todas las tareas.

@app.get("/mostrartareas", tags=['Obtener todas las tareas'])
def leerTareas():
    return {"Estas son las tareas registradas: ": tareas}

# Obtener una tarea específica por su ID.
@app.get("/tareas/{id}", tags=['Obtener una tarea específica por su ID'])
def buscarTarea(id: Optional[int]=None):
    if id is not None:
        for homework in tareas:
            if homework ["id"]==id:
                return {"mensaje": "Tarea :", "tarea":homework}
        return {"mensaje":f"tarea no encontrada, id : {id}"}
    else:
        return {"mensaje":"no ha ingresado un id"}

# Crear una nueva tarea.
@app.post("/tareas", tags=["Crear una nueva tarea"])
def crearTareas(nuevaTarea: dict):
    for homework in tareas:
        if homework ["id"]==nuevaTarea.get("id"):
            raise HTTPException (status_code=400, detail ="esta tarea ya existe")
    tareas.append(nuevaTarea)
    return tareas

# Actualizar una tarea existente.
@app.put("/tareas/{id}", tags=["Actualizar una tarea existente"])
def actualizarTarea(id: int, tareaactualizada: dict):
    for homework in tareas:
        if homework ["id"]== id:
            homework.update(tareaactualizada)
            return {"mensaje": "La tarea ha sido actualizada", "Tarea :":homework}
    raise HTTPException (status_code=400, detail="no se encontro la tarea ingresada")

# Eliminar una tarea.
@app.delete("/tareas/{id}", tags=["Eliminar una tarea"])
def borrarTarea(id:int):
    for homework in tareas:
        if homework["id"]==id:
            tareas.remove(homework)
            return {"mensaje": "Tarea eliminada de la lista", "tarea": homework}
    raise HTTPException (status_code=400, detail=f"no se encontro la tarea con el id: {id}")
