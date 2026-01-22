import streamlit as st
import requests
import pandas as pd

API = "http://127.0.0.1:8000"

st.set_page_config(page_title="Reading Tracker", layout="wide")

if "user_id" not in st.session_state:
    st.session_state.user_id = None

st.title("Reading Tracker")

if not st.session_state.user_id:
    tab1, tab2 = st.tabs(["Login", "Sign up"])

    with tab1:
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        if st.button("Login"):
            r = requests.post(f"{API}/auth/login", json={"username": u, "password": p})
            if r.status_code == 200:
                st.session_state.user_id = r.json()["user_id"]
                st.experimental_rerun()
            else:
                st.error("Invalid credentials")

    with tab2:
        u = st.text_input("New username")
        p = st.text_input("New password", type="password")
        if st.button("Create account"):
            r = requests.post(f"{API}/auth/signup", json={"username": u, "password": p})
            if r.status_code == 200:
                st.success("Account created")
            else:
                st.error("Username already exists")

else:
    st.caption("Logged in")

    with st.form("add_book"):
        title = st.text_input("Title")
        author = st.text_input("Author")
        status = st.selectbox("Status", ["planned", "reading", "completed"])
        rating = st.slider("Rating", 1, 5, 3)
        review = st.text_area("Review")

        if st.form_submit_button("Save"):
            requests.post(
                f"{API}/books/{st.session_state.user_id}",
                json={
                    "title": title,
                    "author": author,
                    "status": status,
                    "rating": rating if status == "completed" else None,
                    "review": review if status == "completed" else None
                }
            )

    books = requests.get(f"{API}/books/{st.session_state.user_id}").json()
    df = pd.DataFrame(
        books,
        columns=["id","user_id","title","author","status","rating","review"]
    )

    st.subheader("Your Library")
    st.dataframe(df[["title","author","status","rating","review"]])
