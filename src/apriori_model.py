import pandas as pd
from sqlalchemy import create_engine
from mlxtend.frequent_patterns import apriori, association_rules
import os

DB_FILE="market.db"

engine=create_engine(f"sqlite:///{DB_FILE}")

def create_database():

    if not os.path.exists(DB_FILE):

        df=pd.read_csv("data/transactions.csv")

        df.to_sql(
        "transactions",
        engine,
        index=False,
        if_exists="replace"
        )

def run_apriori():

    create_database()

    df=pd.read_sql(
    "SELECT * FROM transactions",
    engine
    )

    basket=pd.crosstab(
    df['TransactionID'],
    df['Product']
    )

    basket=basket>0

    frequent=apriori(
    basket,
    min_support=0.003,
    use_colnames=True
    )

    rules=association_rules(
    frequent,
    metric="confidence",
    min_threshold=0.2
    )

    if rules.empty:

        return pd.DataFrame({
        "support":[0],
        "confidence":[0],
        "lift":[0],
        "antecedents":["None"],
        "consequents":["None"]
        })

    rules['antecedents']=rules['antecedents'].astype(str)
    rules['consequents']=rules['consequents'].astype(str)

    return rules.sort_values(
    "lift",
    ascending=False
    )