import requests
from multiprocessing import Pool
from collections import defaultdict
import datetime

# Map Function: Fetches daily temperatures for a given year
def fetch_yearly_data(year):
    latitude = 18.5204   # Pune, India
    longitude = 73.8567
    start_date = f"{year}-01-01"
    end_date = f"{year}-12-31"
    url = (
        f"https://archive-api.open-meteo.com/v1/archive?"
        f"latitude={latitude}&longitude={longitude}"
        f"&start_date={start_date}&end_date={end_date}"
        f"&daily=temperature_2m_max,temperature_2m_min"
        f"&timezone=Asia%2FKolkata"
    )
    try:
        response = requests.get(url)
        data = response.json()
        temps = data['daily']
        max_temp = max(temps['temperature_2m_max'])
        min_temp = min(temps['temperature_2m_min'])
        return (year, min_temp, max_temp)
    except Exception as e:
        print(f"Error fetching data for {year}: {e}")
        return (year, None, None)

# Reduce Function: Determines the hottest and coolest years
def find_extremes(results):

    hottest = max(
        [r for r in results if r[2] is not None],
        key=lambda x: x[2]
    )
    coolest = min(
        [r for r in results if r[1] is not None],
        key=lambda x: x[1]
    )
    return hottest, coolest


if __name__ == "__main__":
    start_year = 2010
    end_year = 2015
    years = list(range(start_year, end_year + 1))

    with Pool() as pool:
        results = pool.map(fetch_yearly_data, years)
    print(results)

    hottest, coolest = find_extremes(results)

    print(f"Hottest Year: {hottest[0]} with max temp {hottest[2]}°C")
    print(f"Coolest Year: {coolest[0]} with min temp {coolest[1]}°C")
