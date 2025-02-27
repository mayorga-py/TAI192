from pydantic import BaseModel, Field, EmailStr

#modelo de validaciones con pydantic
class modeloUsuario (BaseModel):
    id: int = Field(..., gt=0, description="Id unico y solo numeros positivos")
    nombre: str = Field(..., min_length=3, max_length=85, description="solo letras: min 3, max 85")
    edad: int = Field(..., gt=0, lt=120, description="La edad debe ser mayor a 0 y menor que 120")
    email: EmailStr = Field(..., example="algo@correo.com")

#modelo de autentificacion
class modeloAuth (BaseModel):
    email: EmailStr = Field(..., description="correo electronico", example="algo@correo.com")
    passw: str= Field(..., min_length=8, strip_whitespace=True, description="contraseña minimo 8 caracteres")
