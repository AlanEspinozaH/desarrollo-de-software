import json
import os
import sys
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from models import app, db
from models.account import Account
from datetime import date

ACCOUNT_DATA = {}

@pytest.fixture(scope="module", autouse=True)
def setup_database():
    """Mantiene un Application Context activo y crea las tablas una vez."""
    ctx = app.app_context()  # 1) crear el contexto
    ctx.push()               # 2) activarlo para todo el módulo
    db.create_all()          # 3) ya se puede tocar db
    yield                    # --- aquí se ejecutan tus tests ---
    db.session.close()       # 4) cierra la sesión de SQLAlchemy
    ctx.pop()                # 5) sale del contexto al final

class TestAccountModel:
    """Modelo de Pruebas de Cuenta"""

    @classmethod
    def setup_class(cls):
        """Conectar y cargar los datos necesarios para las pruebas"""
        global ACCOUNT_DATA
        with open("tests/fixtures/account_data.json") as json_data:
            ACCOUNT_DATA = json.load(json_data)
        print(f"ACCOUNT_DATA cargado: {ACCOUNT_DATA}")

    @classmethod
    def teardown_class(cls):
        """Desconectar de la base de datos"""
        pass  # Agrega cualquier acción de limpieza si es necesario

    def setup_method(self):
        """Truncar las tablas antes de cada prueba"""
        db.session.query(Account).delete()
        db.session.commit()

    def teardown_method(self):
        """Eliminar la sesión después de cada prueba"""
        db.session.remove()


    def test_create_an_account(self):
        data = {**ACCOUNT_DATA[0], "date_joined": date.today()}
        account = Account(**data)
        account.create()
        assert len(Account.all()) == 1

    def test_create_all_accounts(self):
        for row in ACCOUNT_DATA:
          Account(**{**row, "date_joined": date.today()}).create()
        assert len(Account.all()) == len(ACCOUNT_DATA)