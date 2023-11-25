Django User Authentication API
This project provides a Django-based RESTful API for user registration, email verification, and user login. It supports social media login via Google.

Getting Started
Prerequisites
Python 3.x
Django
PostgreSQL (or your preferred database)
Dependencies (install via pip): Django REST framework, Django Allauth, psycopg2, djangorestframework-simplejwt
Installation
Clone the repository:

bash
Copy code
git clone https://github.com/SoulAbi/User-Authentication-with-Social-Platform-Integration-and-Confirmation-Email.git

cd your-repo

Install dependencies:

bash
Copy code
pip install -r requirements.txt
Apply migrations:

bash
Copy code
python manage.py migrate
Run the development server:

bash
Copy code
python manage.py runserver
API Endpoints
User Registration:

POST /api/register/

json
Copy code
{
    "email": "user@example.com",
    "username": "desired_username",
    "password": "secure_password"
}
Email Verification:

GET /api/verify-email/<token>/

User Login:

POST /api/login/

json
Copy code
{
    "username": "registered_username",
    "password": "user_password"
}
Response Status Codes
200 OK: Successful operation.
400 Bad Request: Invalid or missing parameters.
401 Unauthorized: Incorrect credentials.
404 Not Found: Invalid or expired verification token.
Contributing
Fork the project.
Create your feature branch: git checkout -b feature/YourFeature
Commit your changes: git commit -m 'Add YourFeature'
Push to the branch: git push origin feature/YourFeature
Open a pull request.
License
This project is licensed under the MIT License - see the LICENSE file for details.

Acknowledgments
Django
Django REST framework
Django Allauth
Django REST framework SimpleJWT
