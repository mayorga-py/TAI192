from fastapi import FastAPI,HTTPException,Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
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

Base.metadata.create_all(bind=engine) #crear la tabla en la base de datos


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
@app.get("/todosusuarios", tags=['Operaciones CRUD'])
def leerUsuarios():
    db= Session()
    try:
        consulta= db.query(User).all()
        return JSONResponse (content=jsonable_encoder(consulta))
    except Exception as e:
        return JSONResponse(status_code=500,
                            content={"message":"error al consultar",
                                    "excepcion": str(e) })
    finally:
        db.close()

#buscar por id
@app.get("/usuarios/{id}", tags=['Operaciones CRUD'])
def buscarUno(id:int):
    db=Session()
    try:
        consultauno= db.query(User).filter(User.id == id).first()
        if not consultauno:
            return JSONResponse(status_code=404, content=jsonable_encoder({"mensaje": "usuario no encontrado"}))
        return JSONResponse(content=jsonable_encoder(consultauno))
    except Exception as e:
        return JSONResponse(status_code=500,
                            content={"message":"error al consultar",
                                    "excepcion": str(e) })
    finally:
        db.close()


#endpoit Agregar nuevo usuario
@app.post("/usuarios/", response_model=modeloUsuario, tags=['Operaciones CRUD'])
def agregarUsuarios(usuario: modeloUsuario):
    db=Session()
    #excepciones simepre que se traje con bd
    try:
        db.add(User(**usuario.model_dump()))
        db.commit()
        return JSONResponse(status_code=201,
                            content={"message":"usuario guardado",
                            "usuario": usuario.model_dump() })
    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=500,
                            content={"message":"error al guardar usuario",
                                    "excepcion": str(e) })
    finally:
        db.close()



#endpoit para actualizar un usuario existente
@app.put("/usuarios/{id}", tags=['Operaciones CRUD'])
def actualizarUsuario(id:int, usuario: modeloUsuario):
    db=Session()
    try:
        usuarios = db.query(User).filter(User.id == id).first()
        if not usuarios:
            return JSONResponse(status_code=404, content={"message": "usuario no encontrado"})
        db.query(User).filter(User.id == id).update(usuario.model_dump())
        db.commit()

        usuarioactualizado = db.query(User).filter(User.id == id).first()
        return JSONResponse(content=jsonable_encoder(usuarioactualizado))
    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=500,
                            content={"message":"error al actualizar usuario",
                                    "excepcion": str(e)})
    finally:
        db.close()        

#entpoit parae eliminar usuario por ID
@app.delete("/usuarios/{id}", tags=['Operaciones CRUD'])
def eliminarUsuario(id: int):
    db=Session()
    try:
        usuario = db.query(User).filter(User.id == id).first()
        if not usuario:
            return JSONResponse(status_code=404, content={"message": "usuario no encontrado"})
        
        db.query(User).filter(User.id == id).delete()
        db.commit()
        return JSONResponse(content={"message": "Usuario eliminado correctamente"})
    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=500,
                            content={"message":"error al eliminar usuario",
                                    "excepcion": str(e)})
    finally:
        db.close()


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