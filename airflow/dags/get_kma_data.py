import datetime
import requests
from airflow.decorators import dag
from airflow.operators.python import PythonOperator
from airflow.models.variable import Variable

XCOM_KEY = 'kma_data'
KMA_API_KEY = Variable.get('KMA_API_KEY')
KMA_API_URL = 'https://apihub.kma.go.kr/api/typ01/url/kma_sfcdd.php'

def get_current_hour_data(**context):
    execution_time = context['execution_date']
    tm_value = execution_time.strftime('%Y%m%d%H00')

    params = {
        'tm': tm_value,
        'stn': '0',
        'help': '0',
        'authKey': KMA_API_KEY
    }

    response = requests.get(KMA_API_URL, params=params)
    response.raise_for_status()

    data = response.json()

    context['task_instance'].xcom_push(key=XCOM_KEY, value=data)

def print_kma_data(**context):
    data = context['task_instance'].xcom_pull(key=XCOM_KEY, task_ids='get_kma_data')
    print(f'kma_data: {data}')

@dag(
    start_date=datetime.datetime(2024, 9, 4),
    schedule_interval='@hourly',
    catchup=True
)
def get_kma_dag():
    get_kma_data = PythonOperator(
        task_id='get_kma_data',
        python_callable=get_current_hour_data,
        provide_context=True
    )

    print_kma_data_task = PythonOperator(
        task_id='print_kma_data_task',
        python_callable=print_kma_data,
        provide_context=True
    )

    get_kma_data >> print_kma_data_task

get_kma_dag()
