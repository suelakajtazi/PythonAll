import streamlit as st
import requests 
import pandas as pd

st.title("PROJECT MANAGER APP")
st.header("Add developer")
dev_name = st.text_input("Developer Name")
dev_experience = st.number_input("experience (years)" , min_value=0, max_value=50 , value=0)

if st.button ("creare developer"):
    dev_data = {"name":dev_name,"experience":dev_experience}
    response = requests.post("http://localhost:8000/developers/") #vazhdon


st.header("add project")
pro_title = st.text_input("title")
pro_description = st.text_area("description")
pro_language = st.text_input("language")
lead_developer = st.text_input("developer")
lead_developer_exp = st.number_input("developer experience(years)" , min_value=0, max_value=50 , value=0)

if st.button("create project"):
    lead_dev_data = {"name":lead_developer,"dev_experience":lead_developer_exp}
    pro_data = {
        "title" : pro_title,
        "project description" : pro_description,
        "languages" : pro_language,
        "lead devs" : lead_dev_data
    }
    response = requests.post("http://localhost:8000/developers/", json=pro_data)
    st.json(response.json())


    st.header("project dashboard")
    if st.button("get projects"):
        response = requests.get("http://localhost:8000/developers/")
        pro_data = response.json()['projects']

        if pro_data:
            pro_df = pd.DataFrame(pro_data)


            st.subheader("project overview")
            
            
            
            
            
            
            #to be continued