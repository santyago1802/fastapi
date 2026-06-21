from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
class Cliente(BaseModel):
    id: int
    nombre: str
    edad: int
    email: str
    descripcion: str

Lista_clientes: list[Cliente] = []

@app.get("/clientes")
def listar_clientes():
    return Lista_clientes

#obtner un cliente
@app.get("/clientes/{cliente_id}")
def listar_cliente(cliente_id: int):
    for cliente in Lista_clientes: # ¿porque no se tiene el enumerate y aun asi funciona? Porque no se necesita el indice del cliente, solo se necesita el cliente en si para compararlo con el id que se esta buscando.
        if cliente["id"] == cliente_id:
            return cliente
    return {"error": "Cliente no encontrado"}

#crear un cliente
@app.post("/clientes")
def crear_cliente(datos_cliente: Cliente):
    Lista_clientes.append(datos_cliente)
    return datos_cliente