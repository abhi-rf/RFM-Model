# -*- coding: utf-8 -*-
"""
Created on Tue Oct 31 15:11:13 2017

@author: Dell
"""

from pandas import ExcelFile

df = ExcelFile('C:/Users/Dell/Downloads/Online Retail.xlsx')
df = df.parse('Online Retail')
df.dropna()
columns = df.columns
print(columns)
df = df.groupby(['CustomerID','InvoiceDate'])
#print(len(columns['CustomerID']))
print(df.count())
recency = 10
frequency = 6
monetary = 4