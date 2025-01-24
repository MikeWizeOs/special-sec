Flask 2FA Authentication Example
This project demonstrates the implementation of two-factor authentication (2FA) using Flask. The application includes user registration, login, JWT token generation, token validation, and 2FA support through a secret key. It also includes the ability to send tokens via email (commented out).

Features
User registration with the generation of a 2FA secret key.
User login with username and password verification.
JWT token generation with a limited expiration time.
Token validation via an input form.
Optional token delivery via email (commented out by default).
SQLite database for storing user data.
Installation
1. Clone the repository

git clone <URL_of_your_repository>
cd <repository_folder_name>
2. Install dependencies
Ensure that Python 3 is installed. Install the dependencies using pip:


pip install -r requirements.txt
3. Configure the application
Create a .env file or use environment variables to store sensitive information, such as:

SECRET_KEY — Flask secret key
JWT_SECRET_KEY — Secret key for JWT
Mail server settings (if enabling email functionality).
Example mail configuration:


app.config["MAIL_SERVER"] = "smtp.yourmailserver.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = "your_email@example.com"
app.config["MAIL_PASSWORD"] = "your_password"
4. Set up the database
Before running the application, create the SQLite database:


python
>>> from app import db
>>> db.create_all()
>>> exit()
This will create a users.db file in the root directory of the project.

5. Run the application
Run the Flask application:


python app.py
The application will be available at http://127.0.0.1:5000.

Usage
Registration
Navigate to the registration page: http://127.0.0.1:5000/register.
Enter a username and password.
After successful registration, you will receive a secret key for 2FA. Save this key!
Login
Navigate to the login page: http://127.0.0.1:5000/login.
Enter your username and password.
After successful login, you will receive a JWT token, which you can validate at http://127.0.0.1:5000/token_input.
Token Validation
Enter the token received after login.
If the token is valid, you will see a success message.
Sending Token via Email (Optional)
To enable token delivery via email, uncomment the relevant code in the login function (/login) and configure the mail server.

Project Structure

.
├── app.py                 # Main application file
├── templates/             # HTML templates
│   ├── index.html         # Homepage
│   ├── register.html      # Registration page
│   ├── login.html         # Login page
│   ├── token_input.html   # Token input page
│   └── token.html         # Token display page
├── users.db               # SQLite database (automatically created)
└── requirements.txt       # Python dependencies
Dependencies
Flask
Flask-SQLAlchemy
Flask-JWT-Extended
Flask-Mail
PyOTP
Install them using:


pip install -r requirements.txt
Notes
Ensure that you configure your SMTP settings properly to enable email functionality.
The 2FA secret key is generated using the pyotp library. You can use this key with applications like Google Authenticator for added security.
