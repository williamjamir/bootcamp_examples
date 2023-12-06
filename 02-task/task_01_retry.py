from pathlib import Path

import httpx
from prefect import flow, task, get_run_logger

# Illustrate how to use a task to fetch data from an API


@task
async def fetch_weather(lat: float, lon: float):
    weather = httpx.get(
        url="https://api.open-meteo.com/v1/forecast/",
        params=dict(latitude=lat, longitude=lon, hourly="temperature_2m"),
    )
    return float(weather.json()["hourly"]["temperature_2m"][0])


a = 0


@task(retries=3)
def save_weather(temp: float) -> str:
    logger = get_run_logger()
    global a
    path = Path(f"weather_{a}.csv")
    logger.info(f"Writing text to {path}")

    path.write_text(str(temp))  # Be mindful of idempotency ;)

    if a < 1:
        logger.info("Inside if statement")
        a += 1
        raise ValueError("Test")
    logger.info("Returning from save_weather")
    return "Successfully wrote temp"


@flow
def pipeline(lat: float = 38.9, lon: float = -77.0):
    temp = fetch_weather(lat, lon)
    return save_weather(temp)


if __name__ == "__main__":
    pipeline()
