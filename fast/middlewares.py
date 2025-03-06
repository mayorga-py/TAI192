from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer
from genToken import validateToken

class BearerJWT(HTTPBearer):
    async def __call__ (self, request:Request):
        auth = await super () .__call__(request)

        data = validateToken(auth.credentials)
        if not isinstance(data,dict): #verifica si es un diccionario valido
            raise HTTPException(status_code=401, detail="Token invalido")
        if data.get("email")!= "1@gmail.com": # usar .get para evitar KeyError
            raise HTTPException (status_code=403, detail="credenciales no validas")