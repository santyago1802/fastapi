from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Relationship

class TransaccionBase(SQLModel):
    cantidad: int = Field(default=0)
    vr_unitario: float = Field(default=0.0)
    descripcion: str = Field()

class TransaccionCrear(TransaccionBase):
    pass

class TransaccionEditar(TransaccionBase):
    pass

class Transaccion(TransaccionBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    factura_id: int | None = Field(default=None, foreign_key="factura.id")
    #relacion virtual
    factura : list["Factura"] = Relationship(back_populates="transacciones")

#crear modelo para mostrar al usuario
class Transaccion_leer(TransaccionBase):
    id: int