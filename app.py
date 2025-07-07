import streamlit as st
from utils.form_handler import candidate_form
from utils.file_handler import save_candidate_data

st.set_page_config(page_title="Candidate Evaluation App", layout="centered")
st.title("Candidate Evaluation Form")

# Use a form with session state
if "submitted" not in st.session_state:
    st.session_state.submitted = False

if st.session_state.submitted:
    st.success(" Candidate data saved successfully!")
    if st.button("Add Another Candidate"):
        st.session_state.submitted = False
        st.rerun()
else:
    with st.form("candidate_form"):
        candidate_data, resume_file = candidate_form()
        submitted = st.form_submit_button("Submit and Save")

        if submitted:
            if candidate_data and resume_file:
                save_candidate_data(candidate_data, resume_file)
                st.session_state.submitted = True
                st.rerun()
            else:
                st.error("Please fill in all required fields and upload a resume.")
