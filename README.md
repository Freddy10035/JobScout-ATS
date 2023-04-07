# JobScout-ATS

JobScout-ATS is an Applicant Tracking System (ATS) software built using Python. The software is designed to help companies automate their recruitment processes by providing an efficient way to match job candidates with job vacancies based on their skills and experiences.

The system has the following features:

1. **Resume Parsing:** The software uses open-source libraries like spaCy, NLTK, and PyPDF2 to parse resumes and extract information about the candidate's skills, experience, education, and other relevant details. The parsed data is then stored in a structured format like JSON or XML.
2. **Matching Skills and Jobs:** Once a candidate's resume has been parsed, the software uses OpenAI's language models to match the candidate's skills and experiences with the job requirements available in the company's database.
3. **Providing Job Recommendations:** The software provides job recommendations to the candidate based on their profile. Machine learning algorithms like Collaborative Filtering, Content-Based Filtering, or Hybrid Filtering are used to provide personalized job recommendations.
4. **Accessing Laravel API:** The software accesses the company's Laravel API to retrieve job data from the company's Amazon RDS. A bearer token is generated using the requests library in Python to send a POST request to the Laravel API. The bearer token is then used to send GET requests to retrieve the job data from the Amazon RDS.
5. **Web Application:** The software is built using Flask, a Python web framework. PostgresSQL is used as the database to store the candidate's profiles and job recommendations.

## Installation

To use JobScout-ATS, you need to first clone the repository:

```   
git clone https://github.com/Freddy10035/JobScout-ATS.git
cd JobScout-ATS
```
Next, create a virtual environment and activate it:

````
python -m venv venv
source venv/bin/activate
````

Install the required Python packages:

````
pip install -r requirements.txt
````
Create the PostgresSQL database and tables:

````
psql -c 'CREATE DATABASE job_scout_ats;'
psql -d job_scout_ats -f database/schema.sql
````
Create a .env file with the following variables:

````
FLASK_APP=app.py
FLASK_ENV=development
DATABASE_URL=postgres://<username>:<password>@localhost:5432/job_scout_ats
SECRET_KEY=<your-secret-key>
````

Finally, start the web application:

````
flask run
````
## Usage

The web application has two main functionalities:

1. **Candidate Profile:** Candidates can create their profiles by uploading their resumes. The software parses the resumes and extracts relevant information about the candidate's skills and experiences. The software then matches the candidate's skills and experiences with the job requirements available in the company's database and provides job recommendations to the candidate based on their profile.
2. **Job Dashboard:** Companies can log in and view a dashboard that displays the list of available jobs in the company's database. The job listings can be filtered by job function, job type, and job location. Companies can also view the list of candidates who have applied for each job and view their profiles.

## Contributing

If you would like to contribute to JobScout-ATS, please follow these steps:

1. Fork the repository.
2. Create a new branch and make your changes.
3. Submit a pull request explaining your changes.