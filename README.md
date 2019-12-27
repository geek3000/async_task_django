# Create a sample async task for a django application

To create async task for a django application weed need try package
Django, celeris and redis

## Installation

Use the package manager pip to install it

```bash
pip install Django, celery
pip install redis==2.10.6
apt install redis-server
```

## Configuration
Use this this [tutorial](https://github.com/geek3000/helloWorld_Django) to create a Django App

After, create a file in project_name/project_name directory name it celery.py
```python
import os
from celery import Celery
from django.conf import settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_name.settings')

celery_app = Celery('project_name', broker="redis://localhost:5672/0")
celery_app.config_from_object('django.conf:settings')
celery_app.autodiscover_tasks(settings.INSTALLED_APPS)
```
This will configure Celery. [redis://localhost:5672/0]() is the address of redis-server

Create the __init__.py file and put it in the same directory
```python
from .celery import celery_app

__all__ = ('celery_app',)
```
 Now create tasks.py file in project_name/app_name directory
this file will contain the definition of task
```python
from celery import shared_task

@shared_task
def adding_task(x, y):
    return x + y
```
This fonction (task) will return the sum of two number parameters

## Configure views
First, create template file in project_name/app_name/templates/app_name/views directory
```html
<body>
    <section>
        <div>
            <span class="card-title">HELLO WORLD!!!!</span>
        </div>
		<div>
            <form action="{% url "contact" %}" method="post">
				{% csrf_token %}	
				{{ form.as_p }}
				<input type="submit" value="Submit" />
			</form>
        </div>
		<div>
            <span class="card-title">Result: {{ sum1 }}</span>
        </div>
	</section>
</body>
```
then import package
```python
from django.shortcuts import render
from django.http import HttpResponse
from django import forms
```
Now we create the form containing two inputs
```python
class AddForm(forms.Form):
    nb1 = forms.CharField(max_length=10)
    nb2 = forms.CharField(max_length=10)
```
The most important now views
```python
from .tasks import adding_task
# Create your views here.
def home(request):
    sum1=""
    form = AddForm(request.POST or None)
    if request.method == 'POST':
        
        if form.is_valid(): 
            nb1 = form.cleaned_data['nb1']
            nb2 = form.cleaned_data['nb2']
            try:
                nb1=int(nb1)
                nb2=int(nb2)
                print(nb1, nb2)
                task = adding_task.delay(nb1, nb2)
                sum1=task.get()
            except:
                pass
    return render(request, 'async_app/views/index.html',  locals())
```
Step by step we import the task function, after create the view home
```python
form = AddForm(request.POST or None)
```
if the request method is POST, we get the value of the input, convert it in number and then call the task (in tasks.py) store the result in sum1.
At the end server async_app/views/index.html template and parse it all local object!(form and sum1)

## Launch server

First, start redis-server
```bash
redis-server
```
Secondly, run worker in another terminal(In project root directory
```bash
celery worker -A async --loglevel=info
```
And finally start Django server
```bash
python manage.py runserver
```
## Learn more
See the following link
[tutorial](https://stackabuse.com/asynchronous-tasks-in-django-with-redis-and-celery/)
[tutorial](https://tutorial.djangogirls.org/en/django_forms/)

