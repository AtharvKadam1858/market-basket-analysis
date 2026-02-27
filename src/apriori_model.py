import pandas as pd
from sqlalchemy import create_engine
from mlxtend.frequent_patterns import apriori,association_rules

engine=create_engine("sqlite:///market.db")

def run_apriori():

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