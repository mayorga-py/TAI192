import jwt

def createToken(datos:dict):
    token:str= jwt.endcode(payload=datos, key='secretkey', algortthm='HS256') #encadado de generar el token
    return token

