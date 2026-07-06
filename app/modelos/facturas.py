from pydantic import BaseModel, computed_field
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from app.modelos.clientes import Cliente, Cliente_leer
from app.modelos.transacciones import Transaccion

class FacturaBase(SQLModel):
    fecha: datetime = Field(default=datetime.now())
    #cliente: Cliente
    #transacciones: list[Transaccion] = []


class FacturaCrear(FacturaBase):
    pass

class FacturaEditar(FacturaBase):
    pass

class Factura(FacturaBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    cliente_id: int = Field(default=None, foreign_key="cliente.id")
    #relacion virtual con clientes, transacciones-relaciones virtuales no en la bd
    cliente : Cliente = Relationship(back_populates="factura")
    transacciones : list[Transaccion] = Relationship(back_populates="factura")

#crear modelo para mostrar al usuario 
class Factura_leer(FacturaBase):
    id: int 
    cliente: Cliente_leer
    #se puede agregar transacciones list pero no es recomendable
    #transacciones: list[Transaccion] = []

class Factura_leer_transacciones(FacturaBase):
    id: int
    cliente: Cliente_leer
    transacciones: list[Transaccion] = []

    @computed_field
    @property
    def vr_total(self) -> float:
        total_factura = 0.0
        if self.transacciones == None:
            return total_factura
        for transaccion in self.transacciones:
            total_factura += transaccion.vr_unitario * transaccion.cantidad

        return total_factura
