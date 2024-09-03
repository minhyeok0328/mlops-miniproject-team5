import datetime
import requests
from airflow.decorators import dag
from airflow.operators.python import PythonOperator
from airflow.models.variable import Variable

XCOM_KEY = 'kma_data'
KMA_TOKEN = Variable.get('KMA_TOKEN')
KMA_API_URL = 'https://apihub.kma.go.kr/api/typ01/url/kma_sfctm2.php'

def get_data(**context):
    params = {
        'tm': '202211301000',
        'stn': '0',
        'help': '1',
        'authKey': KMA_TOKEN
    }
    
    response = requests.get(KMA_API_URL, params=params)
    response.raise_for_status()

    data = response.json()

    context['task_instance'].xcom_push(key=XCOM_KEY, value=data)

def print_kma_data(**context):
    data = context['task_instance'].xcom_pull(key=XCOM_KEY, task_ids='print_kma_data')
    print(f'kma_data: {data}')

@dag(
    start_date=datetime.datetime(2025, 7, 24),
    schedule='*/5 * * * *',
    catchup=False
)
def test_kma_dag():
    get_kma_data = PythonOperator(
        task_id='get_kma_data',
        python_callable=get_data,
        provide_context=True
    )

    print_kma_data_task = PythonOperator(
        task_id='print_kma_data_task',
        python_callable=print_kma_data,
        provide_context=True
    )

    get_kma_data >> print_kma_data_task

test_kma_dag()
