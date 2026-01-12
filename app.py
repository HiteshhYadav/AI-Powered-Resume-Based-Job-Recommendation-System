import streamlit as st
from src.helper import extract_text_from_pdf,ask_gemini
from src.job_api import fetch_linkedin_jobs,fetch_naukri_jobs

st.set_page_config(page_title="Job Recommender",layout="wide")
st.title("📄AI Job Recommender")
st.markdown("Upload your resume and get job recommendations based on your skills and experience from LinkedIn and Naukri.")

uploaded_file = st.file_uploader("Upload your resume (PDF format only)", type=["pdf"]) 

if uploaded_file:
    with st.spinner("Extracting text from resume..."):
        resume_text = extract_text_from_pdf(uploaded_file)
    
    with st.spinner("Summarizing your resume..."):
        summary = ask_gemini(f"Summarize this resume highlighting the skills, education and experience : \n\n{resume_text}")
    
    with st.spinner("Finding skill gaps..."):
        gaps = ask_gemini(f"Analyze this resume and highlight missing skills, certifications, and experience needed for better job opportunities: \n\n{resume_text}")

    with st.spinner("Creating Future Roadmap..."):
        roadmap = ask_gemini(f"Based on this resume , suggest a future roadmap to imporve this person's career propects (Skills to learn , certification needed, industry exposure): \n\n{resume_text}")

    st.markdown("---")
    st.header("📝 Resume Summary")
    st.markdown(
        f"""
        <div style="
            background-color:#000000;
            padding:16px;
            border-radius:10px;
            color:white;
            line-height:1.6;
            word-wrap: break-word;
            overflow-wrap: break-word;
            white-space: pre-wrap;
        ">
            {summary}
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("---")
    st.header("🛠️ Skill Gaps & Missing Areas")
    st.markdown(
        f"""
        <div style="
            background-color:#000000;
            padding:16px;
            border-radius:10px;
            color:white;
            line-height:1.6;
            word-wrap: break-word;
            overflow-wrap: break-word;
            white-space: pre-wrap;
        ">
            {gaps}
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")
    st.header("🚀 Future Roadmap & Preparation Strategy")
    st.markdown(
        f"""
        <div style="
            background-color:#000000;
            padding:16px;
            border-radius:10px;
            color:white;
            line-height:1.6;
            word-wrap: break-word;
            overflow-wrap: break-word;
            white-space: pre-wrap;
        ">
            {roadmap}
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.success("✅ Analysis Completed Successfully!")

    if st.button("🔍 Get Job Recommendations"):
        with st.spinner("Fetching job recommendations..."):
            keywords = ask_gemini(f"Based on this resume summary, suggest the best job titles and keywords for searching jobs. Give a comma-separated list only, no explaination. : \n\nSummary:{summary}",max_tokens=100)
       
        search_keywords_clean = keywords.replace("\n","").strip()
        st.success(f"✅ Job Search Keywords Extracted :{search_keywords_clean} ")

        with st.spinner("Fetching jobs from LinkedIn and Naukri..."):
            linkedin_jobs=fetch_linkedin_jobs(search_keywords_clean,rows=60)
            naukri_jobs = fetch_naukri_jobs(search_keywords_clean,rows=60)

        st.markdown("---")
        st.header("💼 Top LinkedIn Jobs")

        if linkedin_jobs:
            for job in linkedin_jobs:
                st.markdown(f"**{job.get('title')}** at *{job.get('companyName')}*")
                st.markdown(f"📍 {job.get('location')}")
                st.markdown(f"🔗 [View Job]({job.get('link')})")
                st.markdown("---")
        else:
            st.warning("No LinkedIn jobs found.")

        st.markdown("---")
        st.header("💼 Top Naukri Jobs (India)")

        if naukri_jobs:
            for job in naukri_jobs:
                st.markdown(f"**{job.get('title')}** at *{job.get('companyName')}*")
                st.markdown(f"📍 {job.get('location')}")
                st.markdown(f"🔗 [View Job]({job.get('link')})")
                st.markdown("---")
        else:
            st.warning("No Naukri jobs found.")


