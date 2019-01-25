# -*- coding: utf-8 -*-
import os
import logging
from datetime import datetime, timedelta

from airflow import models
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.sensors import ExternalTaskSensor
from airflow.contrib.operators.gcs_to_bq import GoogleCloudStorageToBigQueryOperator
from airflow.contrib.operators.dataproc_operator import DataprocClusterCreateOperator
from airflow.contrib.operators.dataproc_operator import DataprocClusterDeleteOperator
from airflow.contrib.operators.dataproc_operator import DataProcPySparkOperator
from airflow.contrib.operators.bigquery_operator import BigQueryOperator
from airflow.contrib.operators.bigquery_to_gcs import BigQueryToCloudStorageOperator

from airflowUtils import join_data_models

DS_SLASH = "{{ macros.ds_format(ds, '%Y-%m-%d', '%Y/%m/%d') }}"

# GCP configuration
# https://cloud.google.com/composer/docs/how-to/managing/connections
GCS_CONNECTION_ID = 'google_cloud_default'
GBQ_CONNECTION_ID = 'bigquery_default'

# GCS
CLUSTER_BUCKET = 'dataproc-d921c7e3-01b3-4556-ba58-5cb4b44e7061' # Pasar a variable
MODEL_BUCKET = 'plp-model-c6d0f40e-ff1f-43e7-811f-1015dba5b2f6' # Pasar a variable

GCS_PATH = f"gs://{MODEL_BUCKET}/train_data"
GCS_PATH_TRAIN_DATA = f"{GCS_PATH}/{DS_SLASH}/table/train/table_master_train_*.csv"
GCS_PATH_VAL_DATA = f"{GCS_PATH}/{DS_SLASH}/table/val/table_master_val_*.csv"
GCS_PATH_TRAIN_SPLIT = f"{GCS_PATH}/{DS_SLASH}/split/train/"
GCS_PATH_VAL_SPLIT = f"{GCS_PATH}/{DS_SLASH}/split/val/"

# BigQuery destination tables
BQ_PROJECT = models.Variable.get('gbq_project')
BQ_DATASET = "03_plp_model_training" # Variable
BQ_MASTER_TABLE = "01_pairwise_training" # Pasar a variable
BQ_TRAIN_TMP = BQ_MASTER_TABLE + "_train_temp"
BQ_VAL_TMP = BQ_MASTER_TABLE + "_val_temp"

# Dataproc
DATAPROC_N_WORKERS = 20
PYSPARK_PY = f'gs://{MODEL_BUCKET}/scripts/split_data.py'

qVal = '''
SELECT
    ID_ESTILO_1,
    ID_ESTILO_2,
    ID_CATEGORY,
    ID_DIA,
    DIF_PRECIO_NORMAL_FTBV_1_7,
    DIF_CANT_VENTA_ACUM_1_7,
    DIF_CANT_VENTA_ACUM_8_14,
    DIF_CANT_VENTA_ACUM_15_21,
    DIF_CANT_VENTA_ACUM_22_28,
    DIF_CANT_VENTA_TIENDA_ACUM_1_7,
    DIF_CANT_VENTA_TIENDA_ACUM_8_14,
    DIF_CANT_VENTA_TIENDA_ACUM_15_21,
    DIF_CANT_VENTA_TIENDA_ACUM_22_28,
    DIF_CANT_VENTA_INTERNET_ACUM_1_7,
    DIF_CANT_VENTA_INTERNET_ACUM_8_14,
    DIF_CANT_VENTA_INTERNET_ACUM_15_21,
    DIF_CANT_VENTA_INTERNET_ACUM_22_28,
    DIF_MONTO_LIQUID_ACUM_1_7,
    DIF_MONTO_LIQUID_ACUM_8_14,
    DIF_MONTO_LIQUID_ACUM_15_21,
    DIF_MONTO_LIQUID_ACUM_22_28,
    DIF_MONTO_LIQUID_TIENDA_ACUM_1_7,
    DIF_MONTO_LIQUID_TIENDA_ACUM_8_14,
    DIF_MONTO_LIQUID_TIENDA_ACUM_15_21,
    DIF_MONTO_LIQUID_TIENDA_ACUM_22_28,
    DIF_MONTO_LIQUID_INTERNET_ACUM_1_7,
    DIF_MONTO_LIQUID_INTERNET_ACUM_8_14,
    DIF_MONTO_LIQUID_INTERNET_ACUM_15_21,
    DIF_MONTO_LIQUID_INTERNET_ACUM_22_28,
    DIF_COMPRADORES_ACUM_1_7,
    DIF_COMPRADORES_ACUM_8_14,
    DIF_COMPRADORES_ACUM_15_21,
    DIF_COMPRADORES_ACUM_22_28,
    DIF_COMPRADORES_TIENDA_ACUM_1_7,
    DIF_COMPRADORES_TIENDA_ACUM_8_14,
    DIF_COMPRADORES_TIENDA_ACUM_15_21,
    DIF_COMPRADORES_TIENDA_ACUM_22_28,
    DIF_COMPRADORES_INTERNET_ACUM_1_7,
    DIF_COMPRADORES_INTERNET_ACUM_8_14,
    DIF_COMPRADORES_INTERNET_ACUM_15_21,
    DIF_COMPRADORES_INTERNET_ACUM_22_28,
    DIF_COMPRAS_CMR_ACUM_1_7,
    DIF_COMPRAS_CMR_ACUM_8_14,
    DIF_COMPRAS_CMR_ACUM_15_21,
    DIF_COMPRAS_CMR_ACUM_22_28,
    DIF_COMPRAS_CMR_TIENDA_ACUM_1_7,
    DIF_COMPRAS_CMR_TIENDA_ACUM_8_14,
    DIF_COMPRAS_CMR_TIENDA_ACUM_15_21,
    DIF_COMPRAS_CMR_TIENDA_ACUM_22_28,
    DIF_COMPRAS_CMR_INTERNET_ACUM_1_7,
    DIF_COMPRAS_CMR_INTERNET_ACUM_8_14,
    DIF_COMPRAS_CMR_INTERNET_ACUM_15_21,
    DIF_COMPRAS_CMR_INTERNET_ACUM_22_28,
    CASE
        WHEN DIF_CANT_VENTA_ACUM_7_0 > 0 THEN 1
        WHEN DIF_CANT_VENTA_ACUM_7_0 < 0 THEN 0
        ELSE NULL
    END AS LABEL
FROM
    `{{ params.table }}`
WHERE
    ID_DIA BETWEEN DATE_ADD(DATE('{{ ds }}'), INTERVAL -14 DAY) AND DATE_ADD(DATE('{{ ds }}'), INTERVAL -8 DAY)
    AND POINT_IN_TIME = DATE('{{ ds }}')
    AND DIF_CANT_VENTA_ACUM_7_0 != 0
'''

qTrain = '''
SELECT
    ID_ESTILO_1,
    ID_ESTILO_2,
    ID_CATEGORY,
    ID_DIA,
    DIF_PRECIO_NORMAL_FTBV_1_7,
    DIF_CANT_VENTA_ACUM_1_7,
    DIF_CANT_VENTA_ACUM_8_14,
    DIF_CANT_VENTA_ACUM_15_21,
    DIF_CANT_VENTA_ACUM_22_28,
    DIF_CANT_VENTA_TIENDA_ACUM_1_7,
    DIF_CANT_VENTA_TIENDA_ACUM_8_14,
    DIF_CANT_VENTA_TIENDA_ACUM_15_21,
    DIF_CANT_VENTA_TIENDA_ACUM_22_28,
    DIF_CANT_VENTA_INTERNET_ACUM_1_7,
    DIF_CANT_VENTA_INTERNET_ACUM_8_14,
    DIF_CANT_VENTA_INTERNET_ACUM_15_21,
    DIF_CANT_VENTA_INTERNET_ACUM_22_28,
    DIF_MONTO_LIQUID_ACUM_1_7,
    DIF_MONTO_LIQUID_ACUM_8_14,
    DIF_MONTO_LIQUID_ACUM_15_21,
    DIF_MONTO_LIQUID_ACUM_22_28,
    DIF_MONTO_LIQUID_TIENDA_ACUM_1_7,
    DIF_MONTO_LIQUID_TIENDA_ACUM_8_14,
    DIF_MONTO_LIQUID_TIENDA_ACUM_15_21,
    DIF_MONTO_LIQUID_TIENDA_ACUM_22_28,
    DIF_MONTO_LIQUID_INTERNET_ACUM_1_7,
    DIF_MONTO_LIQUID_INTERNET_ACUM_8_14,
    DIF_MONTO_LIQUID_INTERNET_ACUM_15_21,
    DIF_MONTO_LIQUID_INTERNET_ACUM_22_28,
    DIF_COMPRADORES_ACUM_1_7,
    DIF_COMPRADORES_ACUM_8_14,
    DIF_COMPRADORES_ACUM_15_21,
    DIF_COMPRADORES_ACUM_22_28,
    DIF_COMPRADORES_TIENDA_ACUM_1_7,
    DIF_COMPRADORES_TIENDA_ACUM_8_14,
    DIF_COMPRADORES_TIENDA_ACUM_15_21,
    DIF_COMPRADORES_TIENDA_ACUM_22_28,
    DIF_COMPRADORES_INTERNET_ACUM_1_7,
    DIF_COMPRADORES_INTERNET_ACUM_8_14,
    DIF_COMPRADORES_INTERNET_ACUM_15_21,
    DIF_COMPRADORES_INTERNET_ACUM_22_28,
    DIF_COMPRAS_CMR_ACUM_1_7,
    DIF_COMPRAS_CMR_ACUM_8_14,
    DIF_COMPRAS_CMR_ACUM_15_21,
    DIF_COMPRAS_CMR_ACUM_22_28,
    DIF_COMPRAS_CMR_TIENDA_ACUM_1_7,
    DIF_COMPRAS_CMR_TIENDA_ACUM_8_14,
    DIF_COMPRAS_CMR_TIENDA_ACUM_15_21,
    DIF_COMPRAS_CMR_TIENDA_ACUM_22_28,
    DIF_COMPRAS_CMR_INTERNET_ACUM_1_7,
    DIF_COMPRAS_CMR_INTERNET_ACUM_8_14,
    DIF_COMPRAS_CMR_INTERNET_ACUM_15_21,
    DIF_COMPRAS_CMR_INTERNET_ACUM_22_28,
    CASE
        WHEN DIF_CANT_VENTA_ACUM_7_0 > 0 THEN 1
        WHEN DIF_CANT_VENTA_ACUM_7_0 < 0 THEN 0
        ELSE NULL
    END AS LABEL
FROM
    `{{ params.table }}`
WHERE
    ID_DIA BETWEEN DATE_ADD(DATE('{{ ds }}'), INTERVAL -43 DAY) AND DATE_ADD(DATE('{{ ds }}'), INTERVAL -23 DAY)
    AND POINT_IN_TIME = DATE('{{ ds }}')
    AND DIF_CANT_VENTA_ACUM_7_0 != 0
'''

# AGREGAR DELETE

default_args = {
    'owner': 'PLP',
    'depends_on_past': False,
    'start_date': datetime(2019, 1, 17),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

with models.DAG(
    'split_train_val',
    default_args=default_args,
    catchup=False,
        schedule_interval='0 9 * * *') as dag:

    t_begin = DummyOperator(
        task_id="Begin"
    )

    s1 = ExternalTaskSensor (
        task_id="PairwiseTrainingSensor",
        external_dag_id="load_pairwise_training",
        external_task_id="Fin"
    )

    t1 = BigQueryOperator(
        task_id='CreateTrainTable',
        bql=qTrain,
        create_disposition='CREATE_IF_NEEDED',
        use_legacy_sql=False,
        write_disposition='WRITE_TRUNCATE',
        destination_dataset_table=f"{BQ_PROJECT}:{BQ_DATASET}.{BQ_TRAIN_TMP}",
        bigquery_conn_id=GBQ_CONNECTION_ID,
        params={
            'table': f"{BQ_PROJECT}.{BQ_DATASET}.{BQ_MASTER_TABLE}"
        }
    )

    t2 = BigQueryOperator(
        task_id='CreateValTable',
        bql=qVal,
        create_disposition='CREATE_IF_NEEDED',
        use_legacy_sql=False,
        write_disposition='WRITE_TRUNCATE',
        destination_dataset_table=f"{BQ_PROJECT}:{BQ_DATASET}.{BQ_VAL_TMP}",
        bigquery_conn_id=GBQ_CONNECTION_ID,
        params={
            'table': f"{BQ_PROJECT}.{BQ_DATASET}.{BQ_MASTER_TABLE}"
        }
    )

    t3 = BigQueryToCloudStorageOperator(
        task_id="ExportTrain",
        source_project_dataset_table=f"{BQ_PROJECT}.{BQ_DATASET}.{BQ_TRAIN_TMP}",
        destination_cloud_storage_uris=[GCS_PATH_TRAIN_DATA],
        export_format='CSV',
        field_delimiter='\t',
        print_header=True,
        bigquery_conn_id=GBQ_CONNECTION_ID
    )

    t4 = BigQueryToCloudStorageOperator(
        task_id="ExportVal",
        source_project_dataset_table=f"{BQ_PROJECT}.{BQ_DATASET}.{BQ_VAL_TMP}",
        destination_cloud_storage_uris=[GCS_PATH_VAL_DATA],
        export_format='CSV',
        field_delimiter='\t',
        print_header=True,
        bigquery_conn_id=GBQ_CONNECTION_ID
    )

    t5 = BashOperator(
        task_id='DeleteTempTrain',
        bash_command='bq rm -f -t {{ params.project }}:{{ params.dataset }}.{{ params.table }}',
        params={
            'project': BQ_PROJECT,
            'dataset': BQ_DATASET,
            'table': BQ_TRAIN_TMP
        }
    )

    t6 = BashOperator(
        task_id='DeleteTempVal',
        bash_command='bq rm -f -t {{ params.project }}:{{ params.dataset }}.{{ params.table }}',
        params={
            'project': BQ_PROJECT,
            'dataset': BQ_DATASET,
            'table': BQ_VAL_TMP
        }
    )

    t7 = DataprocClusterCreateOperator(
        task_id='CreateCluster',
        cluster_name='splittrainval{{ ds_nodash }}',
        project_id=BQ_PROJECT,
        num_workers=int(DATAPROC_N_WORKERS),
        storage_bucket=CLUSTER_BUCKET,
        image_version='1.4.0-RC3-deb9',
        master_machine_type='n1-standard-4',
        worker_machine_type='n1-standard-8',
        zone='us-central1-a',
        auto_delete_ttl=3600,
        service_account_scopes=[
            'https://www.googleapis.com/auth/cloud-platform']
    )

    t8 = DataProcPySparkOperator(
        task_id='SubmitTrainJob',
        main=PYSPARK_PY,
        arguments=[
            str(DATAPROC_N_WORKERS),
            GCS_PATH_TRAIN_DATA,
            GCS_PATH_TRAIN_SPLIT
        ],
        cluster_name='splittrainval{{ ds_nodash }}'
    )

    t9 = DataProcPySparkOperator(
        task_id='SubmitValJob',
        main=PYSPARK_PY,
        arguments=[
            str(DATAPROC_N_WORKERS),
            GCS_PATH_VAL_DATA,
            GCS_PATH_VAL_SPLIT
        ],
        cluster_name='splittrainval{{ ds_nodash }}'
    )

    t10 = DataprocClusterDeleteOperator(
        task_id='DeleteCluster',
        cluster_name='splittrainval{{ ds_nodash }}',
        project_id=BQ_PROJECT
    )

    t_end = DummyOperator(
        task_id="End"
    )

    t_begin >> s1 >> t1 >> t2 >> t3 >> t4 >> t5 >> t6 >> t7 >> t8 >> t9 >> t10 >> t_end
