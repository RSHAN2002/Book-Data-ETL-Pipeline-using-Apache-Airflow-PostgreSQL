from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from dags.tasks.fetch_data import fetch_combined_book_data
from dags.tasks.transform_data import transform_and_enrich_data
from dags.tasks.data_quality import data_quality_checks
from dags.tasks.load_data import load_to_postgres

# DAG Configuration
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2025, 3, 1),
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
}

dag = DAG(
    "book_data_pipeline",
    default_args=default_args,
    description="ETL pipeline for book data",
    schedule_interval="0 9 * * *",  # Runs daily at 9 AM
    catchup=False
)

fetch_combined_task = PythonOperator(
    task_id="fetch_combined_book_data",
    python_callable=fetch_combined_book_data,
    dag=dag
)

transform_task = PythonOperator(
    task_id="transform_and_enrich_data",
    python_callable=transform_and_enrich_data,
    dag=dag
)

quality_check_task = PythonOperator(
    task_id="data_quality_checks",
    python_callable=data_quality_checks,
    dag=dag
)

load_task = PythonOperator(
    task_id="load_to_postgres",
    python_callable=load_to_postgres,
    dag=dag
)

fetch_combined_task >> transform_task >> load_task >> quality_check_task