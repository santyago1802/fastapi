from pydantic import BaseModel

class Cliente_base(BaseModel):
    nombre: str
    edad: int
    email: str
    descripcion: str

class Cliente_crear(Cliente_base):
    pass

class Cliente(Cliente_base):
    id: int | None = None