from django.http import HttpResponse
from django.shortcuts import redirect, render
import requests
# Create your views here.
def home(request):
    query = request.GET.get('query')
    if query:
        return redirect("weather",query = query)
    return render(request,"base.html")

def weather(request,query):
    url = 'http://api.weatherapi.com/v1/forecast.json?key=8bcb19b9d2fe4192a21195756230508&q={}&days=6&aqi=no&alerts=no'
    try:
        if 'query' in request.GET:
            query = request.GET['query']
            r = requests.get(url.format(query)).json()
        else:
            # If 'query' is
            r = requests.get(url.format(query)).json()
        #print(r)
        city_weather = {
            'city' : str(r['location']['name']+", "+r['location']['country']),
            'time' : (r['location']['localtime'])[-5:],
            'temp' : r['current']['temp_c'],
            'text' : r['current']['condition']['text'],
            'wind' : r['current']['wind_kph'],
            'humidity' : r['current']['humidity'],
            'precpitation' : r['current']['precip_in'],
            'img' : r['current']['condition']['icon'],
            'forecast0':{'date':r['forecast']['forecastday'][1]['date'][-2:],
                        'temp':r['forecast']['forecastday'][1]['day']['maxtemp_c'],
                        'img':r['forecast']['forecastday'][1]['day']['condition']['icon']},

            'forecast1':{'date':(r['forecast']['forecastday'][2]['date'])[-2:],
                        'temp':r['forecast']['forecastday'][2]['day']['maxtemp_c'],
                        'img':r['forecast']['forecastday'][2]['day']['condition']['icon']},

            'forecast2':{'date':(r['forecast']['forecastday'][3]['date'])[-2:],
                        'temp':r['forecast']['forecastday'][3]['day']['maxtemp_c'],
                        'img':r['forecast']['forecastday'][3]['day']['condition']['icon']},

            'forecast3':{'date':(r['forecast']['forecastday'][4]['date'])[-2:],
                        'temp':r['forecast']['forecastday'][4]['day']['maxtemp_c'],
                        'img':r['forecast']['forecastday'][4]['day']['condition']['icon']},

            'forecast4':{'date':(r['forecast']['forecastday'][5]['date'])[-2:],
                        'temp':r['forecast']['forecastday'][5]['day']['maxtemp_c'],
                        'img':r['forecast']['forecastday'][5]['day']['condition']['icon']}
        }
        context = {'city_weather': city_weather}
        return render(request,"weather.html",context)
    except KeyError as e:
        # Handle the KeyError by providing an appropriate response to the user
        error_message = "An error occurred while fetching weather data"
        return HttpResponse(error_message, status=500)

    