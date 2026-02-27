import plotly.express as px

def support_chart(rules):

    fig=px.scatter(
    rules,
    x="support",
    y="confidence",
    size="lift",
    hover_data=["antecedents","consequents"],
    title="Association Rules Distribution"
    )

    return fig


def lift_chart(rules):

    top=rules.sort_values(
    "lift",
    ascending=False
    ).head(10)

    fig=px.bar(
    top,
    x="lift",
    y="antecedents",
    orientation="h",
    title="Top Product Associations"
    )

    return fig