from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.postgres.operators.postgres import PostgresOperator
import useful_script


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 3, 28),
}

dag = DAG(
    'PostgreSQL_DAG',
    default_args=default_args,
    schedule_interval='@daily',
)

create_table_task = PostgresOperator(
    task_id='create_table',
    postgres_conn_id='eth_localhost',
    sql='''
        CREATE SCHEMA IF NOT EXISTS erc20_database;

        CREATE TABLE IF NOT EXISTS erc20_database.etherscan_token_data (
            id SERIAL PRIMARY KEY,
            block_number INT,
            date_time TIMESTAMP,
            hash TEXT,
            from_address TEXT,
            to_address TEXT,
            contract_address TEXT,
            value NUMERIC,
            gas NUMERIC,
            gas_price TEXT,
            cumulative_gas_used INT,
            token_name TEXT,
            amount_flag TEXT
        );
    ''',
    dag=dag,
)

def extract_data1(**kwargs):
    sorted_data = useful_script.run_extract('0xdAC17F958D2ee523a2206206994597C13D831ec7') #USDT
    print(sorted_data)
    # push the data
    kwargs['ti'].xcom_push(key='sorted_data_1', value=sorted_data)

def extract_data2(**kwargs):
    sorted_data = useful_script.run_extract('0xB8c77482e45F1F44dE1745F52C74426C631bDD52') #BNB
    print(sorted_data)
    # push the data
    kwargs['ti'].xcom_push(key='sorted_data_2', value=sorted_data)

def extract_data3(**kwargs):
    sorted_data = useful_script.run_extract('0x2b591e99afE9f32eAA6214f7B7629768c40Eeb39') #Hex
    print(sorted_data)
    # push the data
    kwargs['ti'].xcom_push(key='sorted_data_3', value=sorted_data)

def extract_data4(**kwargs):
    sorted_data = useful_script.run_extract('0x95aD61b0a150d79219dCF64E1E6Cc01f0B64C4cE') #SHIBA INU
    print(sorted_data)
    # push the data
    kwargs['ti'].xcom_push(key='sorted_data_4', value=sorted_data)

def extract_data5(**kwargs):
    sorted_data = useful_script.run_extract('0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599') #Wrapped BTC
    print(sorted_data)
    # push the data
    kwargs['ti'].xcom_push(key='sorted_data_5', value=sorted_data)

def transform_data(**kwargs):
    # pull the data
    # sorted_data = kwargs['ti'].xcom_pull(key='sorted_data')
    sorted_data_1 = kwargs['ti'].xcom_pull(key='sorted_data_1')
    sorted_data_2 = kwargs['ti'].xcom_pull(key='sorted_data_2')
    sorted_data_3 = kwargs['ti'].xcom_pull(key='sorted_data_3')
    sorted_data_4 = kwargs['ti'].xcom_pull(key='sorted_data_4')
    sorted_data_5 = kwargs['ti'].xcom_pull(key='sorted_data_5')
    
    # Combine the data from all tasks as necessary
    sorted_data = sorted_data_1 + sorted_data_2 + sorted_data_3 + sorted_data_4 + sorted_data_5

    # Sort the data by datetime
    sorted_data = sorted(sorted_data, key=lambda x: x["dateTime"], reverse=True)

    # Transform data as necessary
    transformed_data = useful_script.run_transform(sorted_data)
    # print(transformed_data)

    # push the data
    kwargs['ti'].xcom_push(key='transformed_data', value=transformed_data)

def load_data(**kwargs):
    transformed_data = kwargs['ti'].xcom_pull(key='transformed_data')
    # Connect to the PostgreSQL database
    conn_id = 'eth_localhost'
    table_name = 'etherscan_token_data'
    schema_name = 'erc20_database'

    insert_sql = f"INSERT INTO {schema_name}.{table_name} (block_number, date_time, hash, from_address, to_address, contract_address, value, gas, gas_price, cumulative_gas_used, token_name, amount_flag) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    #insert_sql = f"INSERT INTO {schema_name}.{table_name} (block_number, date_time, hash, from_address, to_address, contract_address, value, gas, gas_price, cumulative_gas_used, token_name, new_field) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s::bigint, %s, %s, %s)"
    postgres_hook = PostgresHook(postgres_conn_id=conn_id)
    conn = postgres_hook.get_conn()
    cursor = conn.cursor()

    # Execute the insert statement for each row in the transformed data
    for row in transformed_data:
        values = (
            row['blockNumber'],
            row['dateTime'],
            row['hash'],
            row['from'],
            row['to'],
            row['contractAddress'],
            row['value'],
            row['gas'],
            str(row['gasPrice']),
            row['cumulativeGasUsed'],
            row['tokenName'],
            row['amount_flag']
        )
        cursor.execute(insert_sql, values)

    conn.commit()
    cursor.close()
    conn.close()

run_extract_task1 = PythonOperator(
    task_id='run_extract1',
    python_callable=extract_data1,
    dag=dag,
)

run_extract_task2 = PythonOperator(
    task_id='run_extract2',
    python_callable=extract_data2,
    dag=dag,
)

run_extract_task3 = PythonOperator(
    task_id='run_extract3',
    python_callable=extract_data3,
    dag=dag,
)

run_extract_task4 = PythonOperator(
    task_id='run_extract4',
    python_callable=extract_data4,
    dag=dag,
)

run_extract_task5 = PythonOperator(
    task_id='run_extract5',
    python_callable=extract_data5,
    dag=dag,
)

#create_table_task.set_upstream(run_extract_task)

run_transform_task = PythonOperator(
    task_id='run_transform',
    python_callable=transform_data,
    dag=dag,
)

run_load_task = PythonOperator(
    task_id='run_load',
    python_callable=load_data,
    provide_context=True,
    dag=dag,
)

# Flow
create_table_task >> run_extract_task1 >> run_transform_task >> run_load_task
create_table_task >> run_extract_task2 >> run_transform_task >> run_load_task
create_table_task >> run_extract_task3 >> run_transform_task >> run_load_task
create_table_task >> run_extract_task4 >> run_transform_task >> run_load_task
create_table_task >> run_extract_task5 >> run_transform_task >> run_load_task