import unittest
from models import Cuenta
from db import cuentas_db

class TestCuenta(unittest.TestCase):

    def setUp(self):
        self.cuentas = cuentas_db

    def test_pago_exitoso(self):
        cuenta_origen = self.cuentas[0]
        cuenta_destino = self.cuentas[1]
        valor = 100
        
        cuenta_origen.saldo -= valor
        cuenta_destino.saldo += valor
        
        self.assertEqual(cuenta_origen.saldo, 100)
        self.assertEqual(cuenta_destino.saldo, 500)

    def test_saldo_insuficiente(self):
        cuenta_origen = self.cuentas[0]
        valor = 300
        
        with self.assertRaises(Exception):
            if cuenta_origen.saldo < valor:
                raise Exception("Saldo insuficiente")

    def test_contacto_no_existente(self):
        cuenta_origen = self.cuentas[0]
        numerodestino = "789"
        
        with self.assertRaises(Exception):
            if numerodestino not in cuenta_origen.contactos:
                raise Exception("Destino no es un contacto")

    def test_historial_vacio(self):
        cuenta = self.cuentas[0]
        self.assertEqual(len(cuenta.historial), 0)

    def test_anadir_contacto(self):
        cuenta = self.cuentas[0]
        nuevo_contacto = "789"
        cuenta.contactos.append(nuevo_contacto)
        self.assertIn(nuevo_contacto, cuenta.contactos)

if __name__ == "__main__":
    unittest.main()
