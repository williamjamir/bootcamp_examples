from prefect import flow, task
import pandas as pd


@task(task_run_name="TASK 1", persist_result=True)
def my_task():
    print("HELLO FROM TASK 1")
    df = pd.DataFrame(dict(a=[2, 3], b=[4, 5]))
    return df


@task(task_run_name="TASK 2", persist_result=True)
def my_task2(value):
    raise ValueError("Test")


@flow(log_prints=True)
def my_flow():
    res = my_task()
    res2 = my_task2(res)
    return res2


if __name__ == "__main__":
    my_flow.serve(name="william/deploy2")
