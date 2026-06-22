from pydantic import BaseModel, computed_field
from datetime import datetime
from modelos.clientes import Cliente
from modelos.transacciones import Transaccion

class FacturaBase(BaseModel):
    fecha: datetime = datetime.now()
    cliente: Cliente
    transacciones: list[Transaccion] = []

    @computed_field
    @property
    def vr_total(self) -> float:
        total_factura = 0.0

        for transaccion in self.transacciones:
            total_factura += transaccion.vr_unitario * transaccion.cantidad

        return total_factura

class FacturaCrear(FacturaBase):
    pass

class FacturaEditar(FacturaBase):
    pass

class Factura(FacturaBase):
    id: int | None = None