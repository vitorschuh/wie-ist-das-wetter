import os
import re
from os import path

import pandas as pd

from config import EnvLoader
from utils import timeit


@timeit
def get_weather_data(
    api_base: str, api_key: str, city: str, start_date: str, end_date: str
) -> pd.DataFrame:
    """Retrieve weather data from a predefined range as a dataframe."""

    date_pattern = "^\d{4}-\d{2}-\d{2}$"

    for date in [start_date, end_date]:
        match = re.match(date_pattern, date)
        assert match, f"Date '{date}' has not 'YYYY-MM-DD' fmt"

    filters = f"{city}/{start_date}/{end_date}?unitGroup=metric&include=days&key={api_key}&contentType=csv"
    url = path.join(api_base, filters)
    res = pd.read_csv(url)

    return res


@timeit
def main() -> None:
    loader = EnvLoader(prefix="EXTRACT_")
    env = loader.build()
    filepath = path.join(
        env["landing_directory"], f'weekly_{env["start_date"]}_{env["end_date"]}'
    )

    if not path.isdir(filepath):
        os.mkdir(path=filepath)

    df_raw = get_weather_data(
        api_base=env["api_base"],
        api_key=env["api_key"],
        city=env["target_city"],
        start_date=env["start_date"],
        end_date=env["end_date"],
    )

    df_raw.to_csv(path.join(filepath, "weather_measures.csv"), index=False)


if __name__ == "__main__":
    main()
