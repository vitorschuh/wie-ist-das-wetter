import inspect
import time

import pandas as pd
from sqlalchemy import Column, Float, Integer, MetaData, String, Table


def timeit(func: callable) -> callable:
    """
    Decorator that can be applied to any function to measure the execution time of that function.

    Args:
        func (callable): The function to be decorated.

    Returns:
        callable: The resulting decorator function, which includes elapsed time measure to the console.
    """

    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        caller_module = inspect.getframeinfo(inspect.stack()[1][0]).filename.split("/")
        print(
            f"{func.__name__} in {caller_module[-1]} elapsed time: {elapsed_time:.2f} seconds"
        )

        return result

    return wrapper


@timeit
def create_table_from_dataframe(df: pd.DataFrame, table_name: str) -> Table:
    """
    Create a SQLAlchemy table object from a DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame containing the table data.
        table_name (str): The name of the table to be created.

    Returns:
        Table: The created SQLAlchemy table.

    """
    metadata = MetaData()
    columns = [
        Column(
            column_name,
            Float if dtype == "float64" else Integer if dtype == "int64" else String,
        )
        for column_name, dtype in df.dtypes.items()
    ]

    table = Table(table_name, metadata, *columns)

    return table


@timeit
def generate_create_table_ddl(table_name: str, df: pd.DataFrame) -> str:
    """
    Generate a DDL statement to create a table based on the column types of a DataFrame.

    Args:
        table_name (str): The name of the table to be created.
        df (DataFrame): The DataFrame containing the column information.

    Returns:
        str: The DDL statement to create the table.

    """
    ddl_statement = f"CREATE TABLE {table_name} ({', '.join(f'{col} VARCHAR' for col in df.columns)});"

    return ddl_statement
