import streamlit as st

def candidate_form():
    candidate_data = {}

    # Basic Info
    candidate_data["name"] = st.text_input("Candidate Full Name")
    candidate_data["gpa"] = st.number_input("Enter GPA (e.g., 3.5)", min_value=0.0, max_value=4.0, step=0.01)
    resume_file = st.file_uploader("Upload Resume (PDF only)", type=["pdf"])

    # Compulsory Courses
    st.subheader("Compulsory Course Grades")
    compulsory_courses = ["ITC", "PF", "DSA", "DB"]
    grades = {}
    for course in compulsory_courses:
        grades[course] = st.radio(
            f"Grade for {course}",
            ["A", "B", "C", "D", "F"],
            index=1,
            key=f"comp_{course}"
        )

    # Optional Courses - always shown
    st.subheader("Optional Courses (select grade or 'Not Taken')")
    optional_courses = ["ML", "AI", "Data Science"]
    for course in optional_courses:
        grades[course] = st.radio(
            f"Grade for {course}",
            ["A", "B", "C", "D", "F", "Not Taken"],
            index=5,  # default to "Not Taken"
            key=f"opt_{course}"
        )

    candidate_data["grades"] = grades

    # Recommendation
    st.subheader("Final Recommendation")
    candidate_data["recommendation"] = st.radio("Do you recommend this candidate?", ["Yes", "No"])
    candidate_data["remarks"] = st.text_area("Remarks (Why or why not?)")

    return candidate_data if candidate_data["name"] and resume_file else None, resume_file
