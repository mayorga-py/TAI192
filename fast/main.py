from fastapi import FastAPI,HTTPException,Depends
from fastapi.responses import JSONResponse
from typing import Optional, List
from modelsPydantic import modeloUsuario, modeloAuth
from genToken import createToken
from middlewares import BearerJWT
from db.conexion import Session, engine, Base
from models.modelsDB import User


#python -m venv pruebafast

#pip install fastapi uvicorn

#metadatos de la aplicación de FastAPI
app= FastAPI(
    title="mi primer API :D",
    description= "Luis M",
    version= "1.1.2"
) #crear un objeto

# Base de datos simulada (lista de usuarios)
usuarios=[
    {"id": 1, "nombre":"luis", "edad":21, "email":"1@gmail.com"},
    {"id": 2, "nombre":"eduardo", "edad":18,"email":"2@gmail.com"},
    {"id": 3, "nombre":"jose", "edad":20, "email":"3@gmail.com"},
    {"id": 4, "nombre":"karen", "edad":21, "email":"4@gmail.com"},
]

#endpoint home
@app.get("/", tags=['saludo'])
def home():
    return {"message":"bienvenido a FastAPI"}

#endpoint autentificacion
@app.post('/auth', tags=['autentificacion'])
def login(autorizacion: modeloAuth):
    # Validación de credenciales estáticas (debería mejorarse con una base de datos)
    if autorizacion.email == '1@gmail.com' and autorizacion.passw == '123456789':
        token:str = createToken (autorizacion.model_dump()) # Genera el token JWT
        print (token)
        return JSONResponse(content=token)
    else:
        return{"aviso": "Usuario sin autorizacion"}



#endpoint protegido con JWT para obtener todos los usuarios
@app.get("/todosusuarios", dependencies=[Depends(BearerJWT())], response_model= List[modeloUsuario], tags=['Operaciones CRUD'])
def leerUsuarios():
    return usuarios

#endpoit Agregar nuevo usuario
@app.post("/usuarios/", response_model=modeloUsuario, tags=['Operaciones CRUD'])
def agregarUsuarios(nuevo_usuario: modeloUsuario):
    for usr in usuarios:
        if usr ["id"] == nuevo_usuario.id:
            raise HTTPException (status_code=400, detail="este id ya exsiste")
    usuarios.append(nuevo_usuario)
    return usuarios

#endpoit para actualizar un usuario existente
@app.put("/usuarios/{id}", response_model=modeloUsuario, tags=['Operaciones CRUD'])
def actualizarUsuario(id: int, usuarioactualizado: modeloUsuario):
    for index, usr in enumerate (usuarios):
        if usr ["id"]== id:
            usuarios[index]=usuarioactualizado.model_dump()
            return usuarios[index]
        raise HTTPException (status_code=400, detail="no se encontro el usuario")
        
    
#entpoit parae eliminar usuario por ID
@app.delete("/usuarios/{id}", tags=['Operaciones CRUD'])
def eliminarUsuario(id: int):
    for usuario in usuarios:
        if usuario["id"] == id:
            usuarios.remove(usuario)
            return {"mensaje": "usuario eliminado", "usuario": usuario}
    
    raise HTTPException(status_code=400, detail="el usuario no existe, no se puede eliminar")




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