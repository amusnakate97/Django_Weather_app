from django.shortcuts import render,redirect
from django.http import HttpResponse
import requests
from .models import City
from .forms import CityForm
# Create your views here.
def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=f630d0edd9e240e12270207237187cc9'
    message=''
    err_message=''
    message_class=''
    if request.method=='POST':
        form=CityForm(request.POST)

        if form.is_valid():
            new_city=form.cleaned_data['name']
            existing_city_count=City.objects.filter(name=new_city).count()
            if existing_city_count==0:
                r = requests.get(url.format(new_city)).json()
                if r['cod']==200:

                   form.save()
                else:
                    err_message='City does not exist in the world'
            else:
                err_message='City already exists in database'
        if err_message:
            message=err_message
            message_class='is-danger'
        else:
            message='City added successfully'
            message_class='is-success'
    form=CityForm()
    cities=City.objects.all()
    weather_data=[]
    for city in cities:
       r=requests.get(url.format(city)).json()
       city_weather={
        'city':city.name,
        'temperature':r['main']['temp'],
        'description':r['weather'][0]['description'],
        'icon':r['weather'][0]['icon']
        }
       weather_data.append(city_weather)
    print(weather_data)
    context={'weather_data':weather_data,'form':form,'message':message,'message_class':message_class}
    return render(request,'weatherapp/wthr.html',context)
def delete_city(request,city_name):
    City.objects.get(name=city_name).delete()
    return  redirect('home')