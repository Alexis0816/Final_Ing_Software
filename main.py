from fastapi import FastAPI, HTTPException
from db import obtener_cuenta
from models import Historial
from datetime import datetime

app = FastAPI()

@app.get("/billetera/contactos")
def listar_contactos(minumero: str):
    cuenta = obtener_cuenta(minumero)
    if not cuenta:
        raise HTTPException(status_code=404, detail="Cuenta no encontrada")
    return {contacto: obtener_cuenta(contacto).nombre for contacto in cuenta.contactos}

@app.post("/billetera/pagar")
def pagar(minumero: str, numerodestino: str, valor: float):
    cuenta_origen = obtener_cuenta(minumero)
    cuenta_destino = obtener_cuenta(numerodestino)
    
    if not cuenta_origen or not cuenta_destino:
        raise HTTPException(status_code=404, detail="Cuenta no encontrada")
    if numerodestino not in cuenta_origen.contactos:
        raise HTTPException(status_code=400, detail="Destino no es un contacto")
    if cuenta_origen.saldo < valor:
        raise HTTPException(status_code=400, detail="Saldo insuficiente")
    
    fecha_actual = datetime.now().strftime("%d/%m/%Y")
    if cuenta_origen.ultima_fecha_transferencia != fecha_actual:
        cuenta_origen.total_transferido_hoy = 0
        cuenta_origen.ultima_fecha_transferencia = fecha_actual
    
    if cuenta_origen.total_transferido_hoy + valor > 200:
        raise HTTPException(status_code=400, detail="Límite de transferencia diaria excedido")
    
    cuenta_origen.saldo -= valor
    cuenta_destino.saldo += valor
    
    cuenta_origen.total_transferido_hoy += valor
    cuenta_origen.historial.append(Historial("Pago realizado", valor, fecha_actual, numerodestino))
    cuenta_destino.historial.append(Historial("Pago recibido", valor, fecha_actual, minumero))
    
    return {"mensaje": "Pago realizado", "fecha": fecha_actual}

@app.get("/billetera/historial")
def historial(minumero: str):
    cuenta = obtener_cuenta(minumero)
    if not cuenta:
        raise HTTPException(status_code=404, detail="Cuenta no encontrada")
    
    operaciones = [
        {"tipo": h.tipo, "monto": h.monto, "fecha": h.fecha, "contacto": obtener_cuenta(h.contacto).nombre}
        for h in cuenta.historial
    ]
    
    return {"saldo": cuenta.saldo, "operaciones": operaciones}
