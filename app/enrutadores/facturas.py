from fastapi import APIRouter, HTTPException, status
from app.modelos.facturas import Factura, FacturaCrear, FacturaEditar, Factura_leer, Factura_leer_transacciones
from app.modelos.clientes import Cliente
from app.listas import Lista_facturas, Lista_clientes
from app.conexion_bd import Session_dependencia
from sqlmodel import select

rutas_facturas = APIRouter()

@rutas_facturas.get("/facturas", response_model=list[Factura_leer_transacciones])
def listar_facturas(sesion: Session_dependencia):
    #select * from facturas
    consulta = select(Factura)
    Lista_facturas = sesion.exec(consulta).all()
    return Lista_facturas

@rutas_facturas.get("/facturas/{factura_id}", response_model=Factura)
async def listar_factura(factura_id: int):
    for i, obj_factura in enumerate(Lista_facturas):
        if obj_factura.id == factura_id:
            return obj_factura
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"La factura con id {factura_id}, no existe."
    )

@rutas_facturas.post("/facturas/{cliente_id}", response_model=Factura)
async def crear_factura(cliente_id: int, datos_factura: FacturaCrear, sesion: Session_dependencia):
    #buscar el cliente

    cliente_encontrado = sesion.get(Cliente, cliente_id)
    #mensaje si no existe el cliente
    if not cliente_encontrado:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"El cliente con id {cliente_id}, no existe."
        )
    
#validar datos de la factura-json, pasar dict
    factura_dict = datos_factura.model_dump()
    factura_dict["cliente_id"] = cliente_id
    factura_val = Factura.model_validate(factura_dict)

    #guardar en bd
    sesion.add(factura_val)
    sesion.commit()
    sesion.refresh(factura_val)
    return factura_val

@rutas_facturas.patch("/facturas/{factura_id}", response_model=Factura)
async def editar_factura(factura_id: int, datos_factura: FacturaCrear):
    for i, factura in enumerate(Lista_facturas):
        if factura.id == factura_id:
            factura_val = Factura.model_validate(datos_factura.model_dump())
            factura_val.id = factura_id
            Lista_facturas[i] = factura_val
            return factura_val
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"La factura con id {factura_id}, no existe."
    )

@rutas_facturas.delete("/facturas/{factura_id}", response_model=Factura)
async def eliminar_factura(factura_id: int):
    for i, factura in enumerate(Lista_facturas):
        if factura.id == factura_id:
            factura_eliminada = Lista_facturas.pop(i)
            return { "detail": "Factura eliminada", "factura": factura_eliminada }
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"La factura con id {factura_id}, no existe."
    )