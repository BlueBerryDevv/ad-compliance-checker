import pandas as pd
import streamlit as st


df = pd.read_excel("./static/data/患者用医薬品リスト.xlsx")
df.fillna(method='ffill', inplace=True)
df[['企業名_前半', '企業名_後半']] = df['企業名'].str.split('／', n=1, expand=True)


def check_drug(product_name):
    matching_product = df[df['販売名'].str.contains(product_name, case=False, na=False)]

    if not matching_product.empty:
        return 'Safe'
    else:
        return 'Risk'