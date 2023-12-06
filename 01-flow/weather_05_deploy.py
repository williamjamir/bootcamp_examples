import httpx
from prefect import flow, get_run_logger

# Illustrate how to use the `serve` method to deploy a flow

# Deployment contains all metadata needed for remote orchestration
# - When (e.g. schedule, event, etc.)
# - Where (On our server, AWS, GCP, etc.)
# - How (Local process, Docker, Kubernetes, Dask, etc.)

# A flow can have multiple deployments

@flow
def fetch_weather(lat: float = 38.9, lon: float = -77.0):
    weather = httpx.get("https://api.open-meteo.com/v1/forecast/", params=dict(latitude=lat, longitude=lon, hourly="temperature_2m"))
    most_recent_temp = float(weather.json()["hourly"]["temperature_2m"][0])

    print(f"Most recent temp C: {most_recent_temp} degrees")

    logger = get_run_logger()
    logger.info(f"[INFO!] Most recent temp C: {most_recent_temp} degrees")
    logger.debug(f"[DEBUG]! Most recent temp C: {most_recent_temp} degrees")
    logger.warning(f"[WARNING!] Most recent temp C: {most_recent_temp} degrees")
    logger.error(f"[ERROR!] Most recent temp C: {most_recent_temp} degrees")
    logger.critical(f"[CRITICAL!] Most recent temp C: {most_recent_temp} degrees")
    return most_recent_temp


if __name__ == "__main__":
    fetch_weather.serve(name='deploy-1')


# Return to slides
