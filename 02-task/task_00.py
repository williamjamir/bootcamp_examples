from prefect import flow, task
from prefect.tasks import task_input_hash
from datetime import timedelta


@task(cache_key_fn=task_input_hash, cache_expiration=timedelta(minutes=1))
def hello_task(name_input):
    print(f"Hello {name_input}!")


@task(task_run_name="Sleeping for {time}")
async def sleep(time: int) -> int:
    import time as t
    t.sleep(time)
    return time


@task(task_run_name="Doing some stuffs with {value}")
def do_some_stuffs(value):
    print(f"Doing some stuffs with {value}")


@flow(log_prints=True, flow_run_name="MyFlow")  # <--- prints becomes logs
def hello_flow(name_input):

    hello_task(name_input)
    hello_task(name_input)  # <--- This task is cached, therefore it will not run again (prints will not be shown)

    results = sleep.map([5, 1.5])                   # <--- Run all tasks concurrently
    results_2 = [sleep.submit(i) for i in [2, 1]]   # <--- Run all tasks concurrently

    do_some_stuffs(results)
    do_some_stuffs(results_2)  # <--- Wait for all tasks to finish before running this task


if __name__ == "__main__":
    hello_flow("Marvin2")
