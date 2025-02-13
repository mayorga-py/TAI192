from fastapi import FastAPI,HTTPException
from typing import Optional

app= FastAPI (
    title= "API de Gestión de Tareas (To-Do List)",
    description= "por Luis Eduardo Mayorga Becerra",
    version="1.0"
)
tareas=[
    {"id":1 ,"titulo":"respaso de TAI 1", "descripcion":"Repasar los apuntes de TAI", "vencimiento":"14-02-24", "Estado":"completada"},
    {"id":2 ,"titulo":"respaso de TAI 1", "descripcion":"Repasar los apuntes de TAI", "vencimiento":"14-02-24", "Estado":"completada"},
    {"id":3 ,"titulo":"respaso de TAI 1", "descripcion":"Repasar los apuntes de TAI", "vencimiento":"14-02-24", "Estado":"completada"},
    {"id":4 ,"titulo":"respaso de TAI 1", "descripcion":"Repasar los apuntes de TAI", "vencimiento":"14-02-24", "Estado":"completada"},
    {"id":5 ,"titulo":"respaso de TAI 1", "descripcion":"Repasar los apuntes de TAI", "vencimiento":"14-02-24", "Estado":"completada"},
    {"id":6 ,"titulo":"respaso de TAI 1", "descripcion":"Repasar los apuntes de TAI", "vencimiento":"14-02-24", "Estado":"completada"}
]

# Obtener todas las tareas.

@app.get("/mostrartareas", tags=['Endpoints'])
def leerTareas():
    return {"Estas son las tareas registradas: ": tareas}
# Obtener una tarea específica por su ID.
@app.get("/tarea/", tags=['buscar tarea'])
def buscarTarea(id: Optional[int]=None):
    if id is not None:
        for homework in tareas:
            if homework ["id"]==id:
                return {"mensaje": "Tarea :", "tarea":homework}
        return {"mensaje":f"tarea no encontrada, id : {id}"}
    else:
        return {"mensaje":"no a ingresado un id"}

# Crear una nueva tarea.


# Actualizar una tarea existente.


# Eliminar una tarea.