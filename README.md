# CMS
1.Clone this repository  
2. cd to project  
3. prepare your env file in ```envs/.env_dev```  
4. create postgresql db, and update ```config/settings/local.py``` db settings  
5. ```pip install pipenv```  
6. ```pipenv install```  
7.```python manage.py migrate```  
8.create your superuser ```python manage.py createsuperuser```
