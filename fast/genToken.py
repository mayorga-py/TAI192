import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from fastapi import HTTPException

#generar un token con JWT
def createToken(datos:dict):
    token:str= jwt.encode(payload=datos, key='secretkey', algorithm='HS256') #encadado de generar el token y encripta el token con clave secreta
    return token

# Función para validar un token JWT
def validateToken (token:str):
    try:
        data: dict = jwt.decode(token, key="secretkey", algorithms=['HS256'])#desencripta y valida el token
        return data
    except ExpiredSignatureError:
        raise HTTPException(status_code=403, detail="token expirado")
    except InvalidTokenError:
        raise HTTPException(status_code=403, detail="token no autorizado")