from fastapi.responses import JSONResponse
from modelsPydantic import modeloAuth
from genToken import createToken
from middlewares import BearerJWT
from fastapi import APIRouter

routerAuth=APIRouter()

#endpoint autentificacion
@routerAuth.post('/auth', tags=['autentificacion'])
def login(autorizacion: modeloAuth):
    # Validación de credenciales estáticas (debería mejorarse con una base de datos)
    if autorizacion.email == '1@gmail.com' and autorizacion.passw == '123456789':
        token:str = createToken (autorizacion.model_dump()) # Genera el token JWT
        print (token)
        return JSONResponse(content=token)
    else:
        return{"aviso": "Usuario sin autorizacion"}

