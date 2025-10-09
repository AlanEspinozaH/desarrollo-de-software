def test_smoke_import_account():
    from models.account import Account
    a = Account(name="Smoke", email="s@example.com")
    assert a.name == "Smoke"