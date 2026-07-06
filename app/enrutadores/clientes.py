from fastapi import APIRouter, HTTPException, status
from app.modelos.clientes import Cliente, Cliente_crear, Cliente_editar
from app.listas import Lista_clientes
from app.conexion_bd import Session_dependencia
from sqlmodel import select

rutas_clientes = APIRouter()

@rutas_clientes.get("/clientes", response_model=list[Cliente])
async def listar_clientes(session: Session_dependencia):
    lista_cli = session.exec(select(Cliente)).all()
    return lista_cli

#obtner un cliente
@rutas_clientes.get(
        "/clientes/{cliente_id}",
        response_model=Cliente,
)
async def listar_cliente(cliente_id: int, mi_session: Session_dependencia):
    cliente_bd = mi_session.get(Cliente, cliente_id)
    if not cliente_bd:
        raise HTTPException(
            status_code=status.HTTP_404_BAD_REQUEST,
            detail=f"El cliente con id {cliente_id} no existe."
        )
    return cliente_bd

#crear un cliente
@rutas_clientes.post("/clientes", response_model=Cliente)
async def crear_cliente(datos_cliente: Cliente_crear, mi_session: Session_dependencia):
    cliente_val = Cliente.model_validate(datos_cliente.model_dump())
    mi_session.add(cliente_val)
    mi_session.commit()
    mi_session.refresh(cliente_val)
    return cliente_val

@rutas_clientes.patch("/clientes/{cliente_id}", response_model=Cliente)
async def editar_cliente(cliente_id: int,datos_cliente: Cliente_editar, mi_session: Session_dependencia):
    cliente_bd = mi_session.get(Cliente, cliente_id)
    if not cliente_bd:
        raise HTTPException(
            status_code=status.HTTP_404_BAD_REQUEST,
            detail=f"El cliente con id {cliente_id} no existe."
        )
    cliente_dict = datos_cliente.model_dump(exclude_unset=True)
    cliente_bd.sqlmodel_update(cliente_dict)
    mi_session.add(cliente_bd)
    mi_session.commit()
    mi_session.refresh(cliente_bd)
    return cliente_bd


@rutas_clientes.delete("/clientes/{cliente_id}")
async def eliminar_cliente(cliente_id: int, mi_session: Session_dependencia):
    cliente_bd = mi_session.get(Cliente, cliente_id)
    if not cliente_bd:
        raise HTTPException(
            status_code=status.HTTP_404_BAD_REQUEST,
            detail=f"El cliente con id {cliente_id} no existe."
        )
    mi_session.delete(cliente_bd)
    mi_session.commit()
    mi_session.refresh(cliente_bd)
    return cliente_bd