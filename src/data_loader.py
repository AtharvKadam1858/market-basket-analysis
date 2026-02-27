import pandas as pd
from sqlalchemy import create_engine

engine=create_engine("sqlite:///market.db")

df=pd.read_csv("data/transactions.csv")

df.to_sql(
"transactions",
engine,
index=False,
if_exists="replace"
)

print("SQL Database Ready")