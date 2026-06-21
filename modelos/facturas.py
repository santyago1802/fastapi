from pydantic import BaseModel, computed_field
from datetime import datetime
from modelos.clientes import Cliente
from modelos.transacciones import Transaccion

class FacturaBase(BaseModel):
    id: int | None = None
    fecha: datetime = datetime.now()
    cliente: Cliente
    transacciones: list[Transaccion] = []

    @computed_field
    @property
    def vr_total(self) -> float:
        total_factura = 0.0
        factura_id_actual = getattr(self, 'id', None)

        if not factura_id_actual or not self.transacciones:
            return total_factura

        for transaccion in self.transacciones:
            if transaccion.factura_id == factura_id_actual:
                total_factura += transaccion.vr_unitario * transaccion.cantidad

        return total_factura

class FacturaCrear(FacturaBase):
    pass

class FacturaEditar(FacturaBase):
    pass

class Factura(FacturaBase):
    factura_id: int | None = None