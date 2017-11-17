# -*- coding: utf-8 -*-
"""
Created on Tue Oct 31 15:11:13 2017

@author: Dell
"""

from pandas import ExcelFile
import numpy as np
import pandas as pd

encoding='utf-8-sig'

df = ExcelFile('C:/Users/Dell/Downloads/Online Retail.xlsx')
df = df.parse('Online Retail')
df['Total_Price']=df['Quantity']*df['UnitPrice']
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
df['date']=df['InvoiceDate'].dt.year*100+df['InvoiceDate'].dt.month
df.dropna()

columns = df.columns
print(columns)
df = df.groupby(['CustomerID','InvoiceDate'])

print(df.count())
recency = 10
frequency = 6
monetary = 4

Cust_date=df[df['date']]
Cust_date=Cust_date[['CustomerID','date']].drop_duplicates()


def rec(row):
    if row['date'] > 201110:
        val = 5
    elif row['date'] <= 201110 and row['date'] > 201108:
        val = 4
    elif row['date'] <= 201108 and row['date'] > 201106:
        val = 3
    elif row['date'] <= 201106 and row['date'] > 201104:
        val = 2
    else:
        val = 1
    return val*10

Cust_date['Recency_Flag'] = Cust_date.apply(f, axis=1)
Cust_date = Cust_date.groupby("CustomerID",as_index=False)["Recency_Flag"].max()

Cust_freq=df[['Country','InvoiceNo','CustomerID']].drop_duplicates()
Cust_freq_count=Cust_freq.groupby(["Country","CustomerID"])["InvoiceNo"].aggregate("count").reset_index().sort_values('InvoiceNo', ascending=False)

def freq(row):
    if row['InvoiceNo'] <= 13:
        val = 1
    elif row['InvoiceNo'] > 13 and row['InvoiceNo'] <= 25:
        val = 2
    elif row['InvoiceNo'] > 25 and row['InvoiceNo'] <= 38:
        val = 3
    elif row['InvoiceNo'] > 38 and row['InvoiceNo'] <= 55:
        val = 4
    else:
        val = 5
    return val*6

Cust_monetary = df.groupby(["Country","CustomerID"])["Total_Price"].aggregate("sum").reset_index().sort_values('Total_Price', ascending=False)

unique_price=Cust_monetary[['Total_Price']].drop_duplicates()
unique_price=unique_price[unique_price['Total_Price'] > 0]
unique_price['monetary_Band'] = pd.qcut(unique_price['Total_Price'], 5)
unique_price=unique_price[['monetary_Band']].drop_duplicates()

def money(row):
    if row['Total_Price'] <= 243:
        val = 1
    elif row['Total_Price'] > 243 and row['Total_Price'] <= 463:
        val = 2
    elif row['Total_Price'] > 463 and row['Total_Price'] <= 892:
        val = 3
    elif row['Total_Price'] > 892 and row['Total_Price'] <= 1932:
        val = 4
    else:
        val = 5
    return val*4

Cust_All=pd.merge(Cust_date,Cust_freq_count[['CustomerID','Freq_Flag']],on=['CustomerID'],how='left')
Cust_All=pd.merge(Cust_All,Cust_monetary[['CustomerID','Monetary_Flag']],on=['CustomerID'],how='left')
Cust_All.head(10)

Cust_All['RFM_Score']=10*Cust_All['Recency_Flag']+6*Cust_All['Freq_Flag']+4*Cust_All['Monetary_Flag']
Cust_All.head(10)

print(Cust_All['RFM_Score'])