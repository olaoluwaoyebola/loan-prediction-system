import pandas as pd
import sqlite3

df = pd.read_csv("data/loan.csv")

conn = sqlite3.connect("loan.db")

df.to_sql("loans", conn, if_exists="replace", index=False)

print("Data loaded into SQL database")