import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import plotly.express as px
from src.apriori_model import run_apriori

st.set_page_config(
page_title="Market Basket Analytics",
layout="wide"
)

#########################################

st.title("🛒 Market Basket Analytics Dashboard")

st.markdown(
"""
### Cross-Sell Intelligence System

✔ Apriori Algorithm  
✔ SQL Database  
✔ 100,000+ Transactions  
✔ Interactive Dashboard
"""
)

rules=run_apriori()

#########################################
# KPI CARDS
#########################################

st.subheader("Business KPIs")

c1,c2,c3,c4=st.columns(4)

c1.metric("Transactions","100K+")

c2.metric(
"Products",
len(set(rules['antecedents']))
)

c3.metric(
"Association Rules",
len(rules)
)

c4.metric(
"Highest Lift",
round(rules['lift'].max(),2)
)

st.divider()

#########################################
# FILTERS
#########################################

st.sidebar.title("Dashboard Filters")

support_filter=st.sidebar.slider(
"Minimum Support",
0.0,
0.1,
0.01
)

confidence_filter=st.sidebar.slider(
"Minimum Confidence",
0.0,
1.0,
0.2
)

filtered=rules[
(rules['support']>=support_filter)&
(rules['confidence']>=confidence_filter)
]

#########################################
# MAIN CHARTS
#########################################

col1,col2=st.columns(2)

with col1:

    st.subheader("Support vs Confidence")

    fig1=px.scatter(
    filtered,
    x="support",
    y="confidence",
    size="lift",
    hover_data=["antecedents","consequents"]
    )

    st.plotly_chart(
    fig1,
    use_container_width=True
    )


with col2:

    st.subheader("Top Associations")

    top=filtered.sort_values(
    "lift",
    ascending=False
    ).head(10)

    fig2=px.bar(
    top,
    x="lift",
    y="antecedents",
    orientation="h"
    )

    st.plotly_chart(
    fig2,
    use_container_width=True
    )

#########################################
# RULE TABLE
#########################################

st.subheader("Association Rules")

st.dataframe(
filtered,
use_container_width=True
)

#########################################
# PRODUCT RECOMMENDER
#########################################

st.subheader("Product Recommendation Engine")

product=st.selectbox(
"Choose Product",
sorted(set(filtered['antecedents']))
)

recommend=filtered[
filtered['antecedents']
.str.contains(product)
]

st.table(
recommend[
['antecedents',
'consequents',
'confidence',
'lift']
].head(10)
)

#########################################
# AUTO INSIGHTS (VERY IMPRESSIVE)
#########################################

st.subheader("Business Insights")

best=rules.iloc[0]

st.write(
f"""
Customers who buy **{best['antecedents']}**
often also buy **{best['consequents']}**.

Confidence Level:

{round(best['confidence']*100,1)}%

Lift Value:

{round(best['lift'],2)}

This indicates strong cross-selling opportunity.
"""
)

#########################################
# DOWNLOAD
#########################################

st.subheader("Export Results")

csv=rules.to_csv(index=False)

st.download_button(
"Download CSV",
csv,
"market_basket_rules.csv"
)