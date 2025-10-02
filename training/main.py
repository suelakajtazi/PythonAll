
import streamlit as st
import pandas as pd

injuries = pd.read_csv('file.csv')

number = injuries.shape[0]
age = injuries['age'].mean()
never_count = injuries[injuries['smoking_status'] == 'Never'].shape[0]
f_count = injuries[injuries['smoking_status'] == 'Former'].shape[0]

st.title('How many people approximately get diabetes?')
st.write(f'That’s a question that’s rarely asked since around {number:,} get it.')
st.write(f'And most of them do at around the age {age:.1f}.')
# st.write(f'Around {never_count:,} people never smoked.')
# st.write(f'Around {f_count:,} people formaly smoked.')


col1 ,col2 = st.columns(2)

with col1:
    st.header("people who never smoked")
    st.write(never_count)

with col2:
    st.header("people whosmoked")
    st.write(f_count)