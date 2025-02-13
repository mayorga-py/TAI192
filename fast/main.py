from fastapi import FastAPI,HTTPException 
from typing import Optional
app= FastAPI(
    title="mi promer API :D",
    description= "Luis M",
    version= "1.1"
) #crear un objeto
usuarios=[
    {"id": 1, "nombre":"luis", "edad":21},
    {"id": 2, "nombre":"eduardo", "edad":18},
    {"id": 3, "nombre":"jose", "edad":20},
    {"id": 4, "nombre":"karen", "edad":21},
]

#endpoint home
@app.get("/", tags=['saludo'])
def home():
    return {"message":"bienvenido a FastAPI"}

#endpoit usuarios
@app.get("/todosusuarios", tags=['Operaciones CRUD'])
def leerUsuarios():
    return {"Los usuarios registrados son :": usuarios}

#endpoit Agregar nuevo usuario
@app.post("/usuarios/", tags=['Operaciones CRUD'])
def agregarUsuarios(nuevo_usuario: dict):
    for usr in usuarios:
        if usr ["id"] == nuevo_usuario.get("id"):
            raise HTTPException (status_code=400, detail="este id ya exsiste")
    usuarios.append(nuevo_usuario)
    return usuarios

#endpoit
@app.put("/usuarios/{id}", tags=['Operaciones CRUD'])
def actualizarUsuario(id: int, usuarioactualizado: dict):
    for usuario in usuarios:
        if usuario ["id"]== id:
            usuario.update(usuarioactualizado)
            return {"mensaje": "se actualizo el usuario", "usuario": usuario}
        raise HTTPException (status_code=400, detail="no se encontro el usuario")
        
    
#entpoit parae eliminar usuario
@app.delete("/usuarios/{id}", tags=['Operaciones CRUD'])
def eliminarUsuario(id: int):
    for usuario in usuarios:
        if usuario["id"] == id:
            usuarios.remove(usuario)
            return {"mensaje": "usuario eliminado", "usuario": usuario}
    
    raise HTTPException(status_code=404, detail="el usuario no existe, no se puede eliminar")




"""
#endpoint numero
@app.get("/promedio", tags=['numeros y asi'])
def promedio():
    return 5.22
#endpoint parametro onligatorio
@app.get("/usuario/{is}", tags=['parametro obligattorio'])
def consultaUsuario(id:int):
    #conectar a la BD
    #consultamos
    return {'se encontro usurio':id}

#endpoint parametro opcional
@app.get("/usuario/", tags=['parametro opcional'])
def consultaUsuario2(id: Optional[int]= None):
    if id is not None:
        for usu in usuarios:
            if usu ["id"] == id:
                return {"mensaje":"Usuario encontrado", "usuario": usu}

        return {"menaje":f"Usuario no encontrado, id : {id}"}
    else: 
        return {"mensaje":"no se proporciono un id"}



#endpoint con varios parametro opcionales
@app.get("/usuarios/", tags=["3 parámetros opcionales"])
async def consulta_usuarios(
    usuario_id: Optional[int] = None,
    nombre: Optional[str] = None,
    edad: Optional[int] = None
):
    resultados = []

    for usuario in usuarios:
        if (
            (usuario_id is None or usuario["id"] == usuario_id) and
            (nombre is None or usuario["nombre"].lower() == nombre.lower()) and
            (edad is None or usuario["edad"] == edad)
        ):
            resultados.append(usuario)

    if resultados:
        return {"usuarios_encontrados": resultados}
    else:
        return {"mensaje": "No se encontraron usuarios que coincidan con los parámetros proporcionados."}
"""