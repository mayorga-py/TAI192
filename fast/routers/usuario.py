from fastapi import HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from modelsPydantic import modeloUsuario, modeloAuth
from genToken import createToken
from middlewares import BearerJWT
from db.conexion import Session
from models.modelsDB import User
from fastapi import APIRouter

routerUsuario=APIRouter()

#endpoint protegido con JWT para obtener todos los usuarios
@routerUsuario.get("/todosusuarios", tags=['Operaciones CRUD'])
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
@routerUsuario.get("/usuarios/{id}", tags=['Operaciones CRUD'])
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
@routerUsuario.post("/usuarios/", response_model=modeloUsuario, tags=['Operaciones CRUD'])
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
@routerUsuario.put("/usuarios/{id}", tags=['Operaciones CRUD'])
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
@routerUsuario.delete("/usuarios/{id}", tags=['Operaciones CRUD'])
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
