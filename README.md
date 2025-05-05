# Vocabulary App (backend)

Vocabulary App (frontend): [repository](https://github.com/AniaPitera/vocabulary-app-frontend)

# Setup Guide

## Requirements
- Python 3.10
- PostgreSQL

## Steps to Setup the Project

1. **Clone the Repository**
    ```sh
    git clone https://github.com/Nydeyas/vocabulary-app-backend.git
    ```

2. **Create a Virtual Environment**

    Make sure you have Python 3.10 installed.
    Create and enter a virtual environment using:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use venv\Scripts\activate
    ```

4. **Install Dependencies**
   
    ```sh
    cd vocabulary-app-backend
    pip install -r requirements.txt
    ```

6. **Create a PostgreSQL Database**

   Use a tool like pgAdmin4 to create an empty PostgreSQL database. Note down the database name, user, and password.

8. **Create an .env File**

   Create a `.env` file in the `vocabulary-app-backend/vocabulary_app/` directory with the following content:
    ```env
    # Example .env configuration for your Django application
    
    # Django secret key for cryptographic signing
    SECRET_KEY=3kfkqa-9-zvwa!wstk^lpqgykj&swfkc+!ec8j20uszgcr+vn*
    # PostgreSQL database name
    DB_NAME=<NAME>
    # PostgreSQL database username
    DB_USER=postgres
    # PostgreSQL database password
    DB_PASS=<PASSWORD>
    # PostgreSQL database host
    DB_HOST=localhost
    # PostgreSQL database port
    DB_PORT=5432
    # SSL mode for PostgreSQL connection (disable for local setup)
    DB_SSLMODE=disable
    # Debug mode for Django application
    DEBUG=True
    # Allowed hosts for Django application
    ALLOWED_HOSTS=127.0.0.1,localhost
    # CORS allowed origins (include URLs for your frontend application or testing tools, e.g., Postman is 5555)
    CORS_ALLOWED_ORIGINS=http://localhost:5555,http://localhost:2241
    ```

   Make sure to replace placeholders `<NAME>` and `<PASSWORD>` with your actual database credentials.

10. **Create and Apply Migrations**
    ```sh
    python manage.py makemigrations
    python manage.py migrate
    ```

11. **Run the server**
    ```sh
    python runserver.py
    ```

## Testing the Backend

You can test the backend application using Postman:
1. **Register a User**: Send a POST request to `/api/register` to add a new user.
2. **Login**: Send a POST request to `/api/login` to obtain a login token.

With the authentication token (bearer token), you can access the following endpoints and test the methods GET, POST, PUT, DELETE:

- **/api/user**
- **/api/category**
- **/api/word**
- **/api/user/<int>**
- **/api/category/<int>**
- **/api/word/<int>**

For example:
- To list all users: Send a GET request to `/api/user`
- To create a new category: Send a POST request to `/api/category`
- To update a word: Send a PUT request to `/api/word/<int>`
- To delete a user: Send a DELETE request to `/api/user/<int>`

Ensure you include the bearer token in the Authorization header for all these requests.
