Serverless Resume Builder on AWS

A serverless resume management application built using Python, AWS Lambda, Amazon DynamoDB, and HTML, CSS, and JavaScript. The project provides REST API functionality and a user-friendly web interface for creating, managing, previewing, and downloading professional resumes.

Project Overview

The Serverless Resume Builder allows users to enter their personal information, education, work experience, and technical skills through a web-based form.

The backend processes resume information through API endpoints, while the frontend provides an interactive interface with a resume preview and PDF download through the browser's print functionality.

Features

- User-friendly resume builder interface.
- Personal information management.
- Education details management.
- Work experience management.
- Technical skills management.
- REST API integration.
- API key authentication.
- Resume data retrieval using GET requests.
- Resume data submission using POST requests in the local server.
- Dynamic resume preview.
- PDF download using browser print functionality.
- Local development environment with simulated DynamoDB.

Technology Stack

Frontend

- HTML5
- CSS3
- JavaScript

Backend

- Python
- AWS Lambda
- Amazon DynamoDB
- Boto3
- REST API

Development Tools

- Visual Studio Code
- Git
- GitHub
- Python Virtual Environment

Project Structure

Serverless-Resume-API-on-AWS/
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── src/
│   ├── lambda_function.py
│   ├── load_resume.py
│   ├── resume.json
│   └── requirements.txt
│
├── tests/
│   └── test_lambda.py
│
├── local_server.py
├── template.yaml
├── README.md
└── .gitignore

Installation and Setup

1. Clone the Repository

git clone https://github.com/bechani468pal/Serverless-Resume-API-on-AWS.git

2. Navigate to the Project Directory

cd Serverless-Resume-API-on-AWS

3. Create a Virtual Environment

python -m venv venv

4. Activate the Virtual Environment

Windows PowerShell:

.\venv\Scripts\Activate.ps1

5. Install Dependencies

pip install -r src/requirements.txt

6. Start the Backend Server

python local_server.py

The local API server runs at:

http://127.0.0.1:8000

7. Start the Frontend

Open another terminal and run:

npx http-server frontend -p 8081

Open the application in your browser:

http://127.0.0.1:8081

API Endpoints

The local API supports the following GET endpoints:

Method| Endpoint| Description
GET| "/resume"| Retrieve complete resume
GET| "/personal"| Retrieve personal information
GET| "/education"| Retrieve education details
GET| "/experience"| Retrieve work experience
GET| "/skills"| Retrieve technical skills
POST| "/resume"| Submit resume information through the local server

API Authentication

The local development API uses an API key:

demo-resume-key

Pass it using the following request header:

x-api-key: demo-resume-key

Note: The local API key is for demonstration purposes only. Use secure environment-based credentials before public deployment.

How to Use

1. Start the backend and frontend servers.
2. Open the Resume Builder website.
3. Enter your personal information.
4. Add education details.
5. Enter work experience.
6. Add technical skills.
7. Click Save & Generate Resume.
8. Preview the generated resume.
9. Use Download PDF to save the resume through the browser's print dialog.

AWS Architecture

The intended serverless architecture uses:

- AWS Lambda for backend execution.
- Amazon DynamoDB for resume data storage.
- API endpoints for accessing resume information.

The current local development environment uses a Python-based DynamoDB simulator and JSON file storage. AWS deployment requires configuring the appropriate cloud resources and permissions.

Future Enhancements

- AWS cloud deployment.
- Secure user authentication.
- Multiple user resume management.
- Resume templates and customization.
- Direct PDF generation.
- Cloud-based persistent storage.
- Improved form validation.

Learning Outcomes

This project demonstrates practical experience with:

- Serverless application development.
- Python backend programming.
- REST API development.
- AWS Lambda and DynamoDB concepts.
- Frontend and backend integration.
- JSON data management.
- Git and GitHub version control.

Author

Developed as a Serverless Resume API and Resume Builder project.

License

This project is intended for educational and learning purposes.
