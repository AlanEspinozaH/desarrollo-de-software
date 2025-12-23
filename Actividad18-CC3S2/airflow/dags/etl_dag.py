"""
DAG simple que ejecuta el pipeline ETL dentro del contenedor Airflow.

En entorno real usaríamos KubernetesPodOperator / DockerOperator / etc.
Aquí hacemos un PythonOperator directo para demostrar idea.
"""

from datetime import datetime, timedelta  # Importante: importar timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import sys

# Aseguramos que Airflow vea el código del ETL
# (Esto funciona porque en docker-compose.yml montamos ./app en /opt/airflow/app)
sys.path.append("/opt/airflow/app")

try:
    from pipeline import run_etl  # noqa: E402
except ImportError:
    # Bloque de seguridad por si el volumen no está montado al momento de parsear
    def run_etl():
        print("Error: pipeline.py no encontrado en /opt/airflow/app")

with DAG(
    dag_id="etl_pipeline_demo",
    start_date=datetime(2025, 1, 1),
    schedule="@daily",
    catchup=False,
    default_args={"owner": "devsecops"},
    tags=["devsecops", "etl"],
) as dag:

    run_etl_task = PythonOperator(
        task_id="run_etl",
        python_callable=run_etl,
        # REQUISITO 4.3: Timeout para evitar procesos colgados
        execution_timeout=timedelta(minutes=5),
    )