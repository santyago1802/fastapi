from fastapi import FastAPI, HTTPException
from modelos.clientes import Cliente, Cliente_crear
from pydantic import BaseModel, computed_field
from modelos.transacciones import Transaccion, TransaccionCrear
from datetime import datetime
from modelos.facturas import Factura, FacturaCrear, FacturaEditar

app = FastAPI()

Lista_clientes: list[Cliente] = []
Lista_facturas: list[Factura] = []
Lista_transacciones: list[Transaccion] = []

@app.get("/clientes", response_model=list[Cliente])
def listar_clientes():
    return Lista_clientes

#obtner un cliente
@app.get("/clientes/{cliente_id}", response_model=Cliente)
def listar_cliente(cliente_id: int):
    for cliente in Lista_clientes: # ¿porque no se tiene el enumerate y aun asi funciona? Porque no se necesita el indice del cliente, solo se necesita el cliente en si para compararlo con el id que se esta buscando.
        if cliente["id"] == cliente_id:
            return cliente
    return {"error": "Cliente no encontrado"}

#crear un cliente
@app.post("/clientes", response_model=Cliente)
def crear_cliente(datos_cliente: Cliente_crear):
    cliente_val = Cliente.model_validate(datos_cliente.model_dump())
    Lista_clientes.append(cliente_val)
    return cliente_val

@app.get("/facturas", response_model=list[Factura])
def listar_facturas():
    return Lista_facturas

@app.get("/facturas/{factura_id}", response_model=Factura)
def obtener_factura(factura_id: int):
    for factura in Lista_facturas:
        if factura.id == factura_id:
            return factura

    raise HTTPException(status_code=404, detail="Factura no encontrada")

@app.post("/facturas", response_model=Factura)
def crear_factura(datos_factura: FacturaCrear):
    factura = Factura.model_validate(datos_factura.model_dump())
    Lista_facturas.append(factura)
    return factura

@app.get("/transacciones", response_model=list[Transaccion])
def listar_transacciones():
    return Lista_transacciones

@app.get("/transacciones/{transaccion_id}", response_model=Transaccion)
def obtener_transaccion(transaccion_id: int):
    for transaccion in Lista_transacciones:
        if transaccion.id == transaccion_id:
            return transaccion

    raise HTTPException(status_code=404, detail="Transacción no encontrada")

@app.post("/transacciones", response_model=Transaccion)
def crear_transaccion(datos_transaccion: TransaccionCrear):
    transaccion = Transaccion.model_validate(datos_transaccion.model_dump())
    Lista_transacciones.append(transaccion)
    return transaccion