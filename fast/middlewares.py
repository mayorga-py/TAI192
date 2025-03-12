from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer
from genToken import validateToken

#Middleware para validar tokens JWT en las peticiones
class BearerJWT(HTTPBearer):
    async def __call__ (self, request:Request):
        auth = await super () .__call__(request) #0btiene el token de la cabecera

        data = validateToken(auth.credentials)#Valida el token
        if not isinstance(data,dict): #verifica si lainformación es valida (un diccionario en este caso)
            raise HTTPException(status_code=401, detail="Token invalido")
        if data.get("email")!= "1@gmail.com": # usar .get para evitar KeyError para verificar q el email sea el autorizado
            raise HTTPException (status_code=403, detail="credenciales no validas")