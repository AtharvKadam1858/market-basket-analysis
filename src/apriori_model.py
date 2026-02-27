import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
from sqlalchemy import create_engine
from mlxtend.preprocessing import TransactionEncoder

engine = create_engine("sqlite:///data/transactions.db")


def run_apriori():

    try:
        df = pd.read_sql("SELECT * FROM transactions", engine)

        transactions = df.groupby("InvoiceNo")["Description"].apply(list).tolist()

    except:
        # fallback sample data if database missing
        transactions = [
            ["Milk","Bread","Butter"],
            ["Bread","Eggs"],
            ["Milk","Eggs"],
            ["Milk","Bread","Eggs"],
            ["Butter","Bread"]
        ]


    te = TransactionEncoder()
    te_data = te.fit(transactions).transform(transactions)

    basket = pd.DataFrame(te_data, columns=te.columns_)

    frequent_itemsets = apriori(
        basket,
        min_support=0.2,
        use_colnames=True
    )

    rules = association_rules(
        frequent_itemsets,
        metric="lift",
        min_threshold=1
    )

    return rules
