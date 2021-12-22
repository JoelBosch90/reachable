# Django setup instructions
## Set up a Python virtual environment (should not need it in Docker)
`python3 -m venv ~/.virtualenvs/api`
`source ~/.virtualenvs/api/bin/activate`

## Process changes to models
`python manage.py makemigrations`
`python manage.py migrate`

## Run the server
`python manage.py runserver`

# Create an admin user
`python manage.py createsuperuser`