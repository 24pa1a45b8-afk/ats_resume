import os
import streamlit as st
import PyPDF2
import google.generativeai as genai

# ==============================
# PAGE CONFIG
# ==============================

st.set_page_config(
    page_title="ATS Resume Scanner",
    layout="wide"
)

st.title("📄 ATS Resume Scanner with Gemini")

# ==============================
# GEMINI SETUP
# ==============================

# Use Streamlit secrets for security
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

model = genai.GenerativeModel("gemini-2.5-flash")

# ==============================
# PDF TEXT EXTRACTION
# ==============================

def extract_text_from_pdf(uploaded_file):
    text = ""
    reader = PyPDF2.PdfReader(uploaded_file)
    
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted
    
    return text


# ==============================
# RESUME PARSER
# ==============================

def parse_resume(resume_text):

    prompt = f"""
You are a resume parser.

Extract:
- Skills
- Experience summary
- Education
- Tools & technologies

Resume:
{resume_text}

Return in bullet points.
"""

    response = model.generate_content(prompt)

    return response.text


# ==============================
# JOB DESCRIPTION PARSER
# ==============================

def parse_job_description(jd_text):

    prompt = f"""
Extract:
- Required skills
- Responsibilities
- Preferred qualifications

Job Description:
{jd_text}

Return in bullet points.
"""

    response = model.generate_content(prompt)

    return response.text


# ==============================
# ATS MATCHING
# ==============================

def ats_match(parsed_resume, parsed_jd):

    prompt = f"""
You are an Applicant Tracking System.

Compare the resume and job description.

Resume:
{parsed_resume}

Job Description:
{parsed_jd}

Provide:

1. Match percentage (0–100%)
2. Matching skills
3. Missing skills
4. Strengths
5. Improvement suggestions
"""

    response = model.generate_content(prompt)

    return response.text


# ==============================
# STREAMLIT UI
# ==============================

uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

job_description = st.text_area("Paste Job Description")

if st.button("Analyze Resume"):

    if uploaded_file is None:
        st.error("Please upload resume")

    elif job_description.strip() == "":
        st.error("Please paste job description")

    else:

        with st.spinner("Analyzing resume..."):

            # Extract text
            resume_text = extract_text_from_pdf(uploaded_file)

            # Parse resume
            parsed_resume = parse_resume(resume_text)

            # Parse JD
            parsed_jd = parse_job_description(job_description)

            # ATS match
            ats_result = ats_match(parsed_resume, parsed_jd)

        # Display results
        st.success("Analysis Complete")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📄 Parsed Resume")
            st.write(parsed_resume)

        with col2:
            st.subheader("📋 Parsed Job Description")
            st.write(parsed_jd)

        st.subheader("🎯 ATS Match Result")
        st.write(ats_result)
