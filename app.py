import requests
import configparser
from flask import Flask, render_template, url_for, request

# api file


def api_url(cityname, api_key):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={cityname}&units=metric&appid={api_key}'
    return url

# api key


def get_api_key():
    config = configparser.ConfigParser()
    config.read('./config.ini')
    api = config['openweather']['API']
    return api


def parseAPI(cityname):
    r = requests.get(api_url(cityname, get_api_key()))
    data = r.json()
    return data


# Flask
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/result', methods=['POST'])
def result():
    cityname = request.form['cityname']

    try:
        # api data
        api_data = parseAPI(cityname)
    except:
        return render_template('error.html')

    # store data
    temp = str(api_data['main']['temp'])
    feels_like = str(api_data['main']['feels_like'])
    pressure = str(api_data['main']['pressure'])
    humidity = str(api_data['main']['humidity'])
    visibility = str(api_data['visibility'] / 1000)
    wind_speed = str(api_data['wind']['speed'])
    # country = str(api_data['sys']['country'])

    return render_template('results.html',
                           cityname=cityname,
                           temp=temp,
                           feels_like=feels_like,
                           pressure=pressure,
                           humidity=humidity,
                           visibility=visibility,
                           wind_speed=wind_speed)


# run server
if __name__ == '__main__':
    app.run(debug=False)
