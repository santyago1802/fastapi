from fastapi import FastAPI, HTTPException
from modelos.clientes import Cliente, Cliente_crear

app = FastAPI()

Lista_clientes: list[Cliente] = []

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