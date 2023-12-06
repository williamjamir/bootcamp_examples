from prefect import flow

# run -> prefect deploy
# Go to dashboard -> flows -> deploy2 -> run
# Check the worker pool


@flow
def pipe2():
    print("hi")
    return None
