import logging
import sqlite3

import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_data_to_sql(csv_path: str = "data/loan.csv", db_path: str = "loan.db"):
    """Load the loan CSV dataset into a SQLite database."""
    try:
        df = pd.read_csv(csv_path)
        logger.info("Loaded %d rows from %s", len(df), csv_path)
    except FileNotFoundError:
        logger.error("CSV file not found: %s", csv_path)
        raise

    conn = sqlite3.connect(db_path)
    try:
        df.to_sql("loans", conn, if_exists="replace", index=False)
        logger.info("Data loaded into SQL database at %s", db_path)
    finally:
        conn.close()


if __name__ == "__main__":
    load_data_to_sql()