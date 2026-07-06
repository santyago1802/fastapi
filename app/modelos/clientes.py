from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Relationship


class Cliente_base(SQLModel):
    nombre: str = Field(default=None)
    edad: int = Field(default=None)
    email: str = Field(default=None)
    descripcion: str | None = Field(default=None)

class Cliente_crear(Cliente_base):
    pass

class Cliente_editar(Cliente_base):
    pass

class Cliente(Cliente_base, table=True):
    id: int | None = Field(default=None, primary_key=True)
    #relacion virtual con factura
    factura : list["Factura"] = Relationship(back_populates="cliente")

class Cliente_leer(Cliente_base):
    id: int