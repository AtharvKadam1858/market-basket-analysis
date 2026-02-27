import streamlit as st
import pandas as pd
import plotly.express as px

from src.apriori_model import run_apriori


#######################################
# PAGE CONFIG
#######################################

st.set_page_config(
    page_title="Market Basket Dashboard",
    layout="wide"
)

st.title("🛒 Market Basket Analytics Dashboard")
st.subheader("Cross-Sell Intelligence System")

st.write("✔ Apriori Algorithm")
st.write("✔ SQL Database")
st.write("✔ Interactive Dashboard")


#######################################
# SIDEBAR FILTERS
#######################################

st.sidebar.header("Dashboard Filters")

min_support = st.sidebar.slider(
    "Minimum Support",
    0.0,
    1.0,
    0.1
)

min_confidence = st.sidebar.slider(
    "Minimum Confidence",
    0.0,
    1.0,
    0.1
)


#######################################
# LOAD RULES
#######################################

rules = run_apriori()

# Convert frozenset → string (CRITICAL FIX)
rules["antecedents"] = rules["antecedents"].astype(str)
rules["consequents"] = rules["consequents"].astype(str)

rules = rules[
    (rules["support"] >= min_support) &
    (rules["confidence"] >= min_confidence)
]


#######################################
# KPI CARDS
#######################################

st.header("Business KPIs")

col1,col2,col3,col4 = st.columns(4)

col1.metric("Transactions","100K+")
col2.metric("Products",6)
col3.metric("Association Rules",len(rules))

if len(rules) > 0:
    col4.metric("Highest Lift",round(rules["lift"].max(),2))
else:
    col4.metric("Highest Lift",0)


#######################################
# CHART
#######################################

st.header("Support vs Confidence")

if len(rules) > 0:

    fig1 = px.scatter(
        rules,
        x="support",
        y="confidence",
        size="lift",
        hover_data=["antecedents","consequents"]
    )

    st.plotly_chart(fig1,use_container_width=True)

else:
    st.warning("No rules found for selected filters")


#######################################
# TABLE
#######################################

st.header("Association Rules")

st.dataframe(rules)
