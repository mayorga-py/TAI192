from fastapi import FastAPI,HTTPException,Depends
from db.conexion import engine, Base
from routers.usuario import routerUsuario 
from routers.auth import routerAuth

#python -m venv pruebafast
#pip install fastapi uvicorn

#metadatos de la aplicación de FastAPI
app= FastAPI(
    title="mi primer API :D",
    description= "Luis M",
    version= "1.1.2"
) #crear un objeto

Base.metadata.create_all(bind=engine) #crear la tabla en la base de datos

"""
# Base de datos simulada (lista de usuarios)
usuarios=[
    {"id": 1, "nombre":"luis", "edad":21, "email":"1@gmail.com"},
    {"id": 2, "nombre":"eduardo", "edad":18,"email":"2@gmail.com"},
    {"id": 3, "nombre":"jose", "edad":20, "email":"3@gmail.com"},
    {"id": 4, "nombre":"karen", "edad":21, "email":"4@gmail.com"},
]"""

#endpoint home
@app.get("/", tags=['saludo'])
def home():
    return {"message":"bienvenido a FastAPI"}

app.include_router(routerAuth)
app.include_router(routerUsuario)




"""
/////////////////////////////////////////////////////////////
#endpoint numero
@app.get("/promedio", tags=['numeros y asi'])
def promedio():
    return 5.22
#endpoint parametro onligatorio
@app.get("/usuario/{is}", tags=['parametro obligattorio'])
def consultaUsuario(id:int):
    #conectar a la BD
    #consultamos
    return {'se encontro usurio':id}

#endpoint parametro opcional
@app.get("/usuario/", tags=['parametro opcional'])
def consultaUsuario2(id: Optional[int]= None):
    if id is not None:
        for usu in usuarios:
            if usu ["id"] == id:
                return {"mensaje":"Usuario encontrado", "usuario": usu}

        return {"menaje":f"Usuario no encontrado, id : {id}"}
    else: 
        return {"mensaje":"no se proporciono un id"}



#endpoint con varios parametro opcionales
@app.get("/usuarios/", tags=["3 parámetros opcionales"])
async def consulta_usuarios(
    usuario_id: Optional[int] = None,
    nombre: Optional[str] = None,
    edad: Optional[int] = None
):
    resultados = []

    for usuario in usuarios:
        if (
            (usuario_id is None or usuario["id"] == usuario_id) and
            (nombre is None or usuario["nombre"].lower() == nombre.lower()) and
            (edad is None or usuario["edad"] == edad)
        ):
            resultados.append(usuario)

    if resultados:
        return {"usuarios_encontrados": resultados}
    else:
        return {"mensaje": "No se encontraron usuarios que coincidan con los parámetros proporcionados."}
"""