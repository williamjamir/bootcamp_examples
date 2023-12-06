import httpx
from prefect import flow, get_run_logger

@flow
def fetch_weather(lat: float = 38.9, lon: float = -77.0) -> float:
    weather = httpx.get(
        "https://api.open-meteo.com/v1/forecast/",
        params=dict(latitude=lat, longitude=lon, hourly="temperature_2m"),
    )
    most_recent_temp = float(weather.json()["hourly"]["temperature_2m"][0])
    print(f"Most recent temp C (PRINT!): {most_recent_temp} degrees")

    logger = get_run_logger()
    logger.info(f"[INFO!] Most recent temp C: {most_recent_temp} degrees")
    logger.debug(f"[DEBUG]! Most recent temp C: {most_recent_temp} degrees")
    logger.warning(f"[WARNING!] Most recent temp C: {most_recent_temp} degrees")
    logger.error(f"[ERROR!] Most recent temp C: {most_recent_temp} degrees")
    logger.critical(f"[CRITICAL!] Most recent temp C: {most_recent_temp} degrees")

    return most_recent_temp


if __name__ == "__main__":
    fetch_weather()