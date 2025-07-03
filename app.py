import streamlit as st
from utils.form_handler import candidate_form
from utils.file_handler import save_candidate_data

st.set_page_config(page_title="Candidate Evaluation App", layout="centered")
st.title("Candidate Evaluation Form")

# Display form and collect data
candidate_data, resume_file = candidate_form()

if st.button("Submit and Save"):
    if candidate_data and resume_file:
        folder_path = save_candidate_data(candidate_data, resume_file)
        st.success(f" Candidate data saved in: {folder_path}")
    else:
        st.error("Please fill in all required fields and upload a resume.")
