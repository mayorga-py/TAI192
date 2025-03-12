from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer
from genToken import validateToken

# Middleware para validar tokens JWT en las peticiones
class BearerJWT(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)  # Obtiene el token de la cabecera

        data = validateToken(auth.credentials)  # Valida el token
        if not isinstance(data, dict):  # Verifica si la información es válida (un diccionario en este caso)
            raise HTTPException(status_code=401, detail="Token invalido")
        if data.get("licencia") != "123123123123":  # Usar .get para evitar KeyError para verificar que la licencia sea la autorizada
            raise HTTPException(status_code=403, detail="credenciales no validas")