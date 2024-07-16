from typing import List

class Cuenta:
    def __init__(self, numero: str, nombre: str, saldo: float, contactos: List[str]):
        self.numero = numero
        self.nombre = nombre
        self.saldo = saldo
        self.contactos = contactos
        self.historial = []
        self.total_transferido_hoy = 0
        self.ultima_fecha_transferencia = None

class Historial:
    def __init__(self, tipo: str, monto: float, fecha: str, contacto: str):
        self.tipo = tipo
        self.monto = monto
        self.fecha = fecha
        self.contacto = contacto
