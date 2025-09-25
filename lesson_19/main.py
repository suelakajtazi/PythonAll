

import streamlit as st
import pandas as pd
import plotly.express as px


books_df = pd.read_csv('file.csv')


st.title("Bestselling Books Analysis")
st.write("This app analyzes the Amazon Top Selling books from 2009 to 2022.")


st.subheader("Summary Statistics")
total_books = books_df.shape[0]
unique_titles = books_df['Name'].nunique()
average_rating = books_df['User Rating'].mean()
average_price = books_df['Price'].mean()


col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Books", total_books)
col2.metric("Unique Titles", unique_titles)
col3.metric("Average Rating", f"{average_rating:.2f}")
col4.metric("Average Price", f"${average_price:.2f}")

st.subheader("statistics")
st.write(books_df.head())

col1 , col2 = st.columns(2 , gap="small")

with col1:
    st.subheader("the top books")
    top_title = books_df["Name"].value_counts().head(10)
    st.bar_chart(top_title)

with col2:
    st.subheader("the top authors")
    top_authors = books_df["Author"].value_counts().head(10)
    st.bar_chart(top_authors)

st.subheader("genre")
fig = px.pie(books_df, names="Genre", title="most liked genre 2009-2022",color="Genre",
             color_discrete_sequence=px.colors.sequential.Plasma)
st.plotly_chart(fig)

st.subheader("top 15 authors")
top_authors = books_df['Author'].value_counts().head(15).reset_index()
top_authors.columns=['Author','Count']

figg = px.bar(top_authors, x='Count', y='Author', orientation='h',
              title='top 15 authors',
              labels={'Count': 'counts of books published','Author':'Author'},
              color = 'Count',color_continuous_scale=px.colors.sequential.Plasma)

st.plotly_chart(figg)

st.sidebar.header("Add a new book data")
with st.sidebar.form("book_form"):
    new_name = st.text_input("Book Name")
    new_author = st.text_input("Author Name")
    new_user_rating = st.slider("User Rating" , 0.0,0.5,0.0,0.1)
    new_reviews = st.number_input("Reviews" , min_value=0 , step=1)
    new_price = st.number_input("price" , min_value=0 , step=1)
    new_year = st.number_input("year" , min_value=2009 , max_value=2022,step=1)
    new_genre = st.selectbox("genre" , books_df['Genre'].unique())
    submit_button = st.form_submit_button(label="add book")


if submit_button:
    new_data = {
        'Name' : new_name,
        'Author' : new_author,
        'User Rating' : new_user_rating,
        'Reviews' : new_reviews,
        'Price' : new_price,
        'Year' : new_year,
        'Genre' : new_genre
    }
    
    books_df = pd.concat([pd.DataFrame(new_data,index=[0]),books_df],ignore_index=True)
    books_df.to_csv('file.csv',index=False)
    st.sidebar.success('new book added')


st.sidebar.header('Filter option')
select_author = st.sidebar.selectbox('select author',['All'] + list(books_df['Author'].unique()))
select_year = st.sidebar.selectbox('select year',['All'] + list(books_df['Year'].unique()))
select_genre = st.sidebar.selectbox('select genre',['All'] + list(books_df['Genre'].unique()))
# min_rating = st.
# vazhdooooooooooo







