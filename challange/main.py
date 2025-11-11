import streamlit as st

st.title("My notes")
st.header("Below you can input new notes")

title = st.text_input("Title of notes")
note = st.text_area("Notes")

st.markdown(
    """   
    <style>
    body {
        background-color: black;
        color: white;
    }
    .stApp {
        background-color: black;
    }
    textarea, input {
        background-color: #222 !important;
        color: white !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

 #qet css e morra ne chat se se disha qysh duhet me incorporate ne python

st.sidebar.title("Menu")
page = st.sidebar.radio("Go to", ["Add Note", "View Notes"])

if st.button("Save Note"):
    if title and note:
        st.session_state["notes"].append({"title": title, "note": note})
        st.success("Note saved!")
    else:
        st.warning("Please fill in both fields before saving.")

#tani kta u msova :)

st.markdown("""
<style>
    .stButton button {
        background-color: #4CAF50;
        color: white;
        border-radius: 5px;
        height: 2.5em;
        width: 100%;
    }
    .stButton button:hover {
        background-color: #45a049;
    }
    textarea, input {
        border-radius: 5px;
        padding: 8px;
    }
</style>
""", unsafe_allow_html=True)

#tash te qikjo e ndreqi opsionin me i view previous notes e di qe skam ban gati sen but ill do better se sdojsha me chat