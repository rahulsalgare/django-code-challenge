# django-code-challenge
#### Setup Steps
##### 1. Install all the dependencies with  
```
pip install -r requirements.txt
```

##### 2. Make migrations
```
python manage.py makemigrations
```

##### 3. Migrate
```
python manage.py migrate
```

##### 4. Runserver
```
python manage.py runserver
```

### Sendgrid
To use sendgrid mail systems, create account in sendgrid. authenticate your email domain and generate SENDGRID_API_KEY. store the api_key as your environment variable.
Insert your email domain in commented section in serializers.py
Also set SENDGRID_SANDBOX_MODE_IN_DEBUG=False 
