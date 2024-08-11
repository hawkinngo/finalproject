from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator
import os

path = os.environ['AIRFLOW_HOME']

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=1)
    }

dag = DAG(
    dag_id='test_dag',
    start_date=datetime(year=2023, month=12, day=11, hour=10),
    schedule_interval="30 */12 * * *",
    default_args=default_args,
    catchup=False
)

task1 = BashOperator(
  task_id='test_bash',
  bash_command=' uname -r',
  dag=dag
)

task1