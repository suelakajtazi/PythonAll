

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
min_rating = st.sidebar.selectbox('minimal user rating',0.0,0.5,0.0,0.1)
max_price = st.sidebar.selectbox('max price',0,books_df['Price'].max())

filtred_books_df = books_df.copy()

if select_author != "All":
    filtred_books_df = filtred_books_df[filtred_books_df['Author']==select_author]
if select_year != "All":
    filtred_books_df = filtred_books_df[filtred_books_df['Year']==int(select_year)]
if select_genre != "All":
    filtred_books_df = filtred_books_df[filtred_books_df['Genre']==select_genre]

filtred_books_df = filtred_books_df[
    (filtred_books_df['User Rating']>=min_rating) & (filtred_books_df['Price']<=max_price)
]

st.subheader("Summary Statistics")
total_books = filtred_books_df.shape[0]
unique_titles = filtred_books_df['Name'].nunique()
average_rating = filtred_books_df['User Rating'].mean()
average_price = filtred_books_df['Price'].mean()

col1 ,col2 ,col3 ,col4 = st.volumns(4)
col1.metric('total books',total_books)
col2.metric('unique titles',unique_titles)
col3.metric('average rating',f"{average_rating: .2f}")
col4.metric('average price',f"{average_price: .2f}")

st.subheader('Dataset preview')
st.write(filtred_books_df.head())

col1 ,col1 = st.columns(2)

with col1:
    st.subheader("top 10 book titles")
    top_titles = filtred_books_df['Name'].value_counts().head(10)
    st.bar_chart(top_titles)

with col2:
    st.subheader("top 10 book authors")
    top_authors = filtred_books_df['Author'].value_counts().head(10)
    st.bar_chart(top_authors)

st.subheader('genre distribution')
fig = px.pie(filtred_books_df, names='genre', title='most liked genre' , color='genre'
             color_discrete_sequence=px.colors_sequential.Plasma)
st.plotly_chart(fig)

st.subheader('number of fiction vs non-fiction books over years')
size = filtred_books_df.groupby(['Year','Genre']).size().reset_index(name ="Count")
fig = px.bar(size, x='Year',y='Count')



