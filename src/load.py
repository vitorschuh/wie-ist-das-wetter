from os import path

import pandas as pd
import sqlalchemy as sa

from config import EnvLoader
from utils import create_table_from_dataframe, generate_create_table_ddl, timeit


@timeit
def main():
    loader = EnvLoader(prefix="LOAD_")
    env = loader.build()
    engine = sa.create_engine(f'postgresql://{env["database_uri"]}')

    df_raw = pd.read_csv(
        path.join(
            env["takeoff_directory"],
            f'weekly_{env["start_date"]}_{env["end_date"]}',
            "weather_measures.csv",
        )
    )

    table = create_table_from_dataframe(df=df_raw, table_name="weather_measures")
    table.create(bind=engine, checkfirst=True)
    df_raw.to_sql(name="weather_measures", con=engine, if_exists="append", index=False)


if __name__ == "__main__":
    main()
