import streamlit as st



# Initialize notes storage
if "notes" not in st.session_state:
    st.session_state["notes"] = []

st.title("My Notes")
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

st.sidebar.title("Menu")
page = st.sidebar.radio("Go to", ["Add Note", "View Notes"])

# Save action
if page == "Add Note":
    if st.button("Save Note"):
        if title and note:
            st.session_state["notes"].append({"title": title, "note": note})
            st.success("Note saved!")
        else:
            st.warning("Please fill in both fields before saving.")

elif page == "View Notes":
    st.subheader("Saved Notes")
    if st.session_state["notes"]:
        for n in st.session_state["notes"]:
            st.markdown(f"### {n['title']}")
            st.write(n['note'])
            st.markdown("---")
    else:
        st.info("No notes saved yet.")

# Styling
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
