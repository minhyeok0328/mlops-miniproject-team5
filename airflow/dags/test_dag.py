import datetime
from airflow.decorators import dag
from airflow.operators.python import PythonOperator

XCOM_KEY = 'test_data'

def get_data(**context):
    data = { 'test': 1234 }
    context['task_instance'].xcom_push(key=XCOM_KEY, value=data)

def print_test(**context):
    data = context['task_instance'].xcom_pull(key=XCOM_KEY, task_ids='print_test')
    print(f'data: {data}')

@dag(
    start_date=datetime.datetime(2025, 7, 24),
    schedule='*/5 * * * *',
    catchup=False
)
def test_dags():
    get_test_task = PythonOperator(
        task_id='get_test_task',
        python_callable=get_data,
        provide_context=True
    )

    print_test_task = PythonOperator(
        task_id='print_test_task',
        python_callable=print_test,
        provide_context=True
    )

    get_test_task >> print_test_task

test_dags()
