## FundM3 Backend
### Setup environmental variables
```bash
cp .env.sample .env
```

### Using pipenv
```bash
mkdir .venv
pipenv --python 3.8
pipenv shell
```

### Install the requirements
```bash
pip install -r requirements/base.txt
```

### Create database tables 
```bash
python manage.py migrate
```

### Create superuser to access admin dashboard
```bash
python manage.py createsuperuser
```

### Run backend server
```bash
python manage.py runserver
```
