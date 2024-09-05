from airflow import Dag
import datetime
import pendulum
from airflow.operators.bash import BashOperator

with DAG(
    dag_id = "install_requests",
    schedule="0 0 1 1 0"
    start_date = pendulum.datetime(2023, 9, 5, tz="Asia/Seoul"),
    catchup=False
)as dag:
    bash_t1 = BashOperator(
        task_id="bash_t1",
        bash_command = "pip install requests"
    )
    bash_t1