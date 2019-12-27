from django.shortcuts import render
from django.http import HttpResponse
from django import forms

class AddForm(forms.Form):
    nb1 = forms.CharField(max_length=10)
    nb2 = forms.CharField(max_length=10)

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
