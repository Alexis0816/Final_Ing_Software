from models import Cuenta

# Inicializar datos
cuentas_db = [
    Cuenta("21345", "Arnaldo", 200, ["123", "456"]),
    Cuenta("123", "Luisa", 400, ["456"]),
    Cuenta("456", "Andrea", 300, ["21345"])
]

def obtener_cuenta(numero: str) -> Cuenta:
    for cuenta in cuentas_db:
        if cuenta.numero == numero:
            return cuenta
    return None
