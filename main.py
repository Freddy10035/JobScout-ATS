import openai
import os

import requests
import spacy
import urllib3
from dotenv import load_dotenv
from urllib3.exceptions import InsecureRequestWarning

# Load environment variables
load_dotenv()

# Set up OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")
model_id = os.getenv("MODEL_ID")

# Set up Spacy
nlp = spacy.load("en_core_web_sm")

# Set up Laravel API bearer token
bearer_token = os.getenv("BEARER_TOKEN")

# Disable SSL certificate verification warnings
urllib3.disable_warnings(InsecureRequestWarning)


# Define functions to get resume skills and job requirements
def get_resume_skills(resume_text):
    resume_doc = nlp(resume_text)
    skills = [ent.text for ent in resume_doc.ents if ent.label_ == "SKILL"]
    return list(set(skills))


def get_job_requirements(requirements_text):
    requirements_doc = nlp(requirements_text)
    requirements = [ent.text for ent in requirements_doc.ents if ent.label_ == "SKILL"]
    return list(set(requirements))


# Define function to get job recommendations
def get_job_recommendations(resume_text):
    # Get skills from resume
    resume_skills = get_resume_skills(resume_text)

    # Get job data from Laravel API
    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "Content-Type": "application/json"
    }
    try:
        jobs_response = requests.get(url="https://localhost/all-jobs-api/api/v1/jobs", headers=headers, verify=False)
        jobs_response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
        jobs = jobs_response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to get job data: {e}")

    # Filter jobs by matching skills
    recommended_jobs = [job for job in jobs if set(resume_skills) & set(get_job_requirements(job["job_requirements"]))]

    # Generate job descriptions prompt
    job_descriptions = "\n".join(job["job_description"] for job in recommended_jobs)
    prompt_with_job_descriptions = f"Based on your resume and our matching algorithm, we recommend the following jobs:\n\n{job_descriptions}"

    # Generate job recommendations using OpenAI GPT model
    response = openai.Completion.create(
        engine=model_id,
        prompt=prompt_with_job_descriptions,
        max_tokens=4096,
        n=1,
        stop=None,
        temperature=0.5
    )

    # Extract recommended jobs from OpenAI GPT response
    recommendations = response.choices[0].text.split("\n")
    recommended_job_links = [recommendations[recommendations.index(job["job_title"]) + 1] for job in recommended_jobs if job["job_title"] in recommendations]

    return recommended_job_links


# Define function to take user input and display job recommendations
def main():
    print("Welcome to JobScout-ATS!\n")
    resume_text = input("Please paste your resume text here: \n")
    try:
        recommended_job_links = get_job_recommendations(resume_text)
        print("Based on your resume and our matching algorithm, we recommend the following jobs:\n")
        for link in recommended_job_links:
            print(link)
    except Exception as e:
        print(f"Error: {e}")
        print("Failed to get job recommendations.")


if __name__ == "__main__":
    main()
