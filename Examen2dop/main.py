from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import Optional, List
from modelsPydantic import modeloUsuario, modeloAuth
from genToken import createToken
from middlewares import BearerJWT

app = FastAPI(
    title="registro conductores",
    description="Luis M",
    version="1.1"
)  # crear un objeto

conductores = [
    {"nombre": "luis", "tipo_licencia": "A", "licencia": 123123123123},
    {"nombre": "eduardo", "tipo_licencia": "B", "licencia": 258258258258},
    {"nombre": "jose", "tipo_licencia": "C", "licencia": 363636363636},
    {"nombre": "karen", "tipo_licencia": "D", "licencia": 474747474747},
]

# Endpoint consulta conductor
@app.get("/conductores/", dependencies=[Depends(BearerJWT())], tags=['parametro opcional'])
def consultaConductores(licencia: Optional[int] = None):
    if licencia is not None:
        licencia_str = str(licencia)
        if len(licencia_str) != 12:
            return {"mensaje": "La licencia debe tener exactamente 12 caracteres"}
        for usu in conductores:
            if usu["licencia"] == licencia:
                return {"mensaje": "Usuario encontrado", "usuario": usu}
        return {"mensaje": f"El conductor no existe: {licencia}"}
    else:
        return {"mensaje": "No se proporcionó una licencia"}

# Nuevo endpoint para buscar conductor por licencia
@app.get("/conductores/{licencia}", dependencies=[Depends(BearerJWT())], tags=['buscar conductor'])
def buscarConductor(licencia: int):
    licencia_str = str(licencia)
    if len(licencia_str) != 12:
        raise HTTPException(status_code=400, detail="La licencia debe tener exactamente 12 caracteres")
    for usu in conductores:
        if usu["licencia"] == licencia:
            return {"mensaje": "Usuario encontrado", "usuario": usu}
    raise HTTPException(status_code=404, detail="El conductor no existe")

@app.post('/auth', tags=['autentificacion'])
def login(autorizacion: modeloAuth):
    # Validación de credenciales estáticas
    if autorizacion.licencia == '123123123123':
        token: str = createToken(autorizacion.model_dump())  # Genera el token JWT
        print(token)
        return JSONResponse(content=token)
    else:
        return {"aviso": "Usuario sin autorizacion"}

@app.get("/todosusuarios", dependencies=[Depends(BearerJWT())], response_model=List[modeloUsuario], tags=['autentificacion'])
def leerConductores():
    return conductores

# Endpoint eliminar por n de licencia
@app.delete("/conductores/{id}", dependencies=[Depends(BearerJWT())], tags=['eliminar conductor'])
def eliminarUsuario(id: int):
    id_str = str(id)
    if len(id_str) != 12:
        raise HTTPException(status_code=400, detail="La licencia debe tener exactamente 12 caracteres")
    for usuario in conductores:
        if usuario["licencia"] == id:
            conductores.remove(usuario)
            return {"mensaje": "Usuario eliminado", "usuario": usuario}
    raise HTTPException(status_code=400, detail="El usuario no existe, no se puede eliminar")