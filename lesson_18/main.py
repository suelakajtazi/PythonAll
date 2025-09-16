import pandas as pd
import streamlit as st
import plotly.express as px

# df = pd.DataFrame({

#       'name':[]

# }
# )

books_df = pd.read_csv('file.csv')

st.title('bestselling books')
st.write('this app shows the bestselling apps on amazone from 2009 to 2022')


st.subheader('book statistics')
total_books = books_df.shape[0]
unique_title = books_df['name'].unique()
average_rating = books_df['user rating'].mean()
average_price = books_df['price'].mean()

col1 , col2 ,col3 ,col4 = st.columns(4)
col1.metric('total books',total_books)
col2.metric('titles',unique_title)
col3.metric('average rating',average_rating)
col4.metric('average price',average_price)

