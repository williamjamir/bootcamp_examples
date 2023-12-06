from prefect import flow, task
import pandas as pd


@task(task_run_name="PERSITED", persist_result=True)
def my_task():
    df = pd.DataFrame(dict(a=[2, 3], b=[4, 5]))
    return df


@task(task_run_name="NOT PERSITED")
def my_task2():
    df = pd.DataFrame(dict(c=[4, 6], d=[8, 10]))
    return df


@task()
def dummy_task(value):
    print(f"value: {value}")


@flow(log_prints=True)
def my_flow():
    res = my_task()
    res2 = my_task2()
    dummy_task(res)
    dummy_task(res2)
    return "success"

# Show storage folder on .prefect
# Show log output from task on the dashboard

if __name__ == "__main__":
    my_flow()
