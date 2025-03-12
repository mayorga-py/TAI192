from pydantic import BaseModel, Field, EmailStr

# Modelo de validaciones de datos para usuarios con pydantic
class modeloUsuario(BaseModel):
    nombre: str = Field(..., min_length=3, description="el nombre debe de llevar como minimo 3 caracteres")
    licencia: int = Field(..., min_length=1, max_length=12, description="la licencia debe de tener 12 caracteres")
    tipo_licencia: str = Field(..., min_length=1, max_length=1, description="solo debe de haber un caracter (A,B,C,D)")

# Modelo de autentificación
class modeloAuth(BaseModel):
    licencia: str = Field(..., description="licencia del conductor", example="123456789123")