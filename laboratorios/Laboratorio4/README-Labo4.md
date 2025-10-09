# 
Creacion del entorno virtual.
cd /ruta/al/repositorio/Laboratorio/Laboratorio4
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip

instalacion de requirements.txt
pip install -r requirements.txt


Para reproducibilidad y que toda maquina pueda instalar las mismas verisones y todo funciones igual
# estando en Laboratorio4 con el venv activo
pip install pip-tools
cp requirements.txt requirements.in
pip-compile --generate-hashes -o requirements.txt requirements.in
pip-sync requirements.txt

# para hacer los ptest de todo (recomendacion: ejecutar pytest por actividad)
pytest -v Actividades


# probar pytest
# 1) limpiar cachés (recomendado una vez)
find . -type d -name '__pycache__' -prune -exec rm -rf {} +
rm -rf .pytest_cache

# 2) correr actividad por actividad
cd Actividades/pruebas_pytest
pytest -q

cd ../aserciones_pruebas
pytest -q

cd ../coverage_pruebas
pytest -q

cd ../factories_fakes
pytest -q

cd ../pruebas_fixtures
pytest -q

cd ../mocking_objetos
pytest -q

# instalar pytest y pytest-cov  
# En la carpeta aserciones_pruebas:
python3 -m pip install pytest pytest-cov
# ejecutar la suite: make test  o el comando:
pytest -v

# Cobertura (terminal/HTML)

Terminal: 
pytest --cov=stack --cov-report=term-missing   # (o make coverage_individual a nivel repo)