from airflow import DAG
from airflow.operators.python import PythonOperator


def run_ai_support_summary():
    print("openai support summary task")


with DAG("support_agent_dag") as dag:
    ai_task = PythonOperator(
        task_id="run_ai_support_summary",
        python_callable=run_ai_support_summary,
    )

