from fastapi import APIRouter, HTTPException,status
from app.modelos.facturas import Factura
from app.modelos.transacciones import Transaccion, TransaccionCrear
from app.listas import Lista_transacciones, Lista_facturas
from app.conexion_bd import Session_dependencia
from sqlmodel import select

rutas_transacciones = APIRouter()

@rutas_transacciones.get("/transacciones", response_model=list[Transaccion])
def listar_transacciones(sesion: Session_dependencia):
    #consulta = select(Transaccion)
    #Lista_transacciones = sesion.exec(consulta).all()
    #return Lista_transacciones
    return sesion.exec(select(Transaccion)).all()

@rutas_transacciones.get("/transacciones/{transaccion_id}", response_model=Transaccion)
def listar_transaccion(transaccion_id: int):
    pass

    raise HTTPException(status_code=404, detail="Transacción no encontrada")

@rutas_transacciones.post("/transacciones/{factura_id}", response_model=Transaccion)
async def crear_transaccion(factura_id: int, datos_transaccion: TransaccionCrear, sesion: Session_dependencia):
    #buscar la factura
    factura_encontrada = sesion.get(Factura, factura_id)
    #mensaje si no existe el cliente
    if not factura_encontrada:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail=f"la factura con id {factura_id}, no existe."
            )
        
    #validar datos de la factura
    transaccion_dict = datos_transaccion.model_dump()
    transaccion_dict["factura_id"] = factura_id
    Transaccion_val = Transaccion.model_validate(transaccion_dict)
    #guardar en bd
    sesion.add(Transaccion_val)
    sesion.commit()
    sesion.refresh(Transaccion_val)
    return Transaccion_val


@rutas_transacciones.patch("/transacciones/{transaccion_id}", response_model=Transaccion)
async def editar_transaccion(transaccion_id: int, datos_transaccion: TransaccionCrear):
    for i, transaccion in enumerate(Lista_transacciones):
        if transaccion.id == transaccion_id:
            transaccion_val = Transaccion.model_validate(datos_transaccion.model_dump())
            transaccion_val.id = transaccion_id
            Lista_transacciones[i] = transaccion_val
            return transaccion_val

@rutas_transacciones.delete("/transacciones/{transaccion_id}", response_model=Transaccion)
async def eliminar_transaccion(transaccion_id: int):
    for i, transaccion in enumerate(Lista_transacciones):
        if transaccion.id == transaccion_id:
            transaccion_eliminada = Lista_transacciones.pop(i)
            return { "detail": "Transacción eliminada", "transaccion": transaccion_eliminada }