Patent Analysis System
A Django-based web application for patent analysis with OpenAI integration.

Overview
This project is a patent analysis system that allows users to:

View and analyze patent data
Search through patent database
Get AI-powered insights using OpenAI integration
Visualize patent trends and relationships
Technologies Used
Backend: Django 4.2
Frontend: Bootstrap 5
Database: SQLite
AI Integration: OpenAI GPT API
Data Format: JSON
Project Structure

my_pp/
├── data/                  # JSON data files
├── management/            # Django management commands
├── services/              # Business logic and AI services
├── static/               # Static files (CSS, JS)
├── templates/            # HTML templates
└── migrations/           # Database migrations
Setup Instructions
Clone the repository:

git clone [repository-url]
Create and activate a virtual environment:

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies:

pip install -r requirements.txt
Set up environment variables:
Create a .env file in the root directory and add:

OPENAI_API_KEY=your_api_key_here
Run database migrations:

python manage.py migrate
Import initial data:

python manage.py import_data
Run the development server:

python manage.py runserver
Data Import
The system uses two main JSON files:

patents.json: Contains patent information
company_products.json: Contains company and product data
To import data, use the management command:


python manage.py import_data
Features
Patent Search
Search by patent number
Search by company name
Full-text search in patent descriptions
AI Analysis
Patent similarity analysis
Trend identification
Technical field classification
Visualization
Patent timeline view
Company relationship graphs
Technology clustering
API Endpoints
/: Home page
/search/: Patent search interface
/analyze/: AI-powered analysis interface
Dependencies
Main dependencies include:

Django
Bootstrap
OpenAI
Python-dotenv
For a complete list, see requirements.txt

Development
To contribute to the project:

Create a new branch
Make your changes
Submit a pull request
Testing
Run tests using:


python manage.py test
Deployment
The application is currently deployed at:


http://222.186.21.40:29630
License
[Your chosen license]

Contact
For any questions or issues, please contact [your contact information]