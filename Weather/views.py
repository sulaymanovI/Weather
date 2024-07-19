from django.shortcuts import render
from .forms import CityForm
from .models import City
import requests


def get_weather(request):
    
    weather_data=None
    error=None

    if request.method == 'POST':
        form=CityForm(request.POST)

        if form.is_valid():
            city=form.cleaned_data['name']
            latitude , longitude =get_coordinates(city)

            if latitude and longitude:
                url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m"
                response = requests.get(url)

                if response.status_code==200:
                    weather_data=response.json()
                    times = weather_data['hourly']['time']
                    temperatures = weather_data['hourly']['temperature_2m']
                    combined_data = list(zip(times, temperatures))

                else:
                    error = 'Could not retrieve weather data'
                
            else:
                error = 'Could not find coordinates for the city'
    else:
        form=CityForm()

    return render(request , 'weather.html' ,  {'form': form,'combined_data': combined_data,'error': error})


def get_coordinates(city):
    api_key = '13e4c4365b7f46dca32a4c8bc0c7fd3e'
    url = f'https://api.opencagedata.com/geocode/v1/json?q={city}&key={api_key}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data['results']:
            coordinates = data['results'][0]['geometry']
            return coordinates['lat'], coordinates['lng']
    return None, None