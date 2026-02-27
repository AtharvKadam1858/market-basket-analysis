import pandas as pd
import random

products=[
"Milk","Bread","Butter","Eggs","Rice","Cheese",
"Chicken","Juice","Apple","Banana",
"Coffee","Tea","Sugar","Salt","Oil"
]

rows=[]

for t in range(100000):

    items=random.sample(products,random.randint(2,6))

    for item in items:

        rows.append([t,item])

df=pd.DataFrame(rows,columns=["TransactionID","Product"])

df.to_csv("transactions.csv",index=False)

print("Dataset Created Successfully")