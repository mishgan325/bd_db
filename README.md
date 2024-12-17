# Project Setup Instructions

1. **Python 3.8+**
2. **MySQL** (configured locally)
3. **pip**

## Setup Steps

### 1. Clone the Repository

```bash
git clone https://github.com/mishgan325/bd_db
cd bd_db
```

### 2. Create a Virtual Environment

Create and activate a Python virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### 3. Install Requirements

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### 4. Configure MySQL

Ensure that MySQL is installed and running locally. Update the database credentials in the project settings.

1. Open the configuration file (e.g., `settings.py` or `.env`).
2. Update the MySQL password and other credentials as needed:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '<database_name>',
        'USER': '<username>',
        'PASSWORD': '<your_password>',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
```

### 5. Apply Migrations

Run the following command to apply database migrations:

```bash
python manage.py migrate
```

### 6. Run the Development Server

Start the server using:

```bash
python manage.py runserver
```

Access the application in your browser at [http://127.0.0.1:8000](http://127.0.0.1:8000).

## Additional Notes

- If you encounter issues connecting to MySQL, verify your credentials and ensure the MySQL server is running.
- Use `python manage.py createsuperuser` to create an admin account for accessing the Django admin panel.
