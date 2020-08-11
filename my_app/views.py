from django.shortcuts import render
from django.http import HttpResponseRedirect

from bs4 import BeautifulSoup
import requests


# Create your views here.


def home(request):
    return render(request, 'my_app/home.html')


def search(request):
    print(request.POST)
    search_text = request.POST['search']
    print(search_text)
    if search_text == "":
        return HttpResponseRedirect("/")
    else:
        search_ = 'weather+' + search_text
        url = "http://www.google.com/search?q=" + search_
        weather_data = get_weather_data(url)
        return render(request, "my_app/search.html", weather_data)


def get_weather_data(url):
    print(url)
    user_agent_desktop = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' \
                         'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 ' \
                         'Safari/537.36'
    html = requests.get(url, headers={'User-Agent': user_agent_desktop})

    # Scrap :D!
    soup = BeautifulSoup(html.text, "html.parser")
    result = {'region': soup.find("div", attrs={"id": "wob_loc"}).text,
              'temp_now': soup.find("span", attrs={"id": "wob_tm"}).text,
              'dayhour': soup.find("div", attrs={"id": "wob_dts"}).text,
              'weather_now': soup.find("span", attrs={"id": "wob_dc"}).text,
              'precipitation': soup.find("span", attrs={"id": "wob_pp"}).text,
              'humidity': soup.find("span", attrs={"id": "wob_hm"}).text,
              'wind': soup.find("span", attrs={"id": "wob_ws"}).text}

    return result
