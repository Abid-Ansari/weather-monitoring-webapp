from flask import Flask, request, redirect ,render_template
import requests 

app = Flask(__name__)
base_url = 'http://api.weatherapi.com/v1/'
url = 'http://api.weatherapi.com/v1/current.json?key=a078339df6874857856153714240111&q=London'
apikey = 'a078339df6874857856153714240111'
headers={'Authorization':f'Bearer {apikey}','Content-Type':'application/json'}

@app.route("/",methods = ['GET','POST'])
def hello_world():
    if request.method == 'POST':
        loc = request.form.get('city')
        current_weather_url = base_url + '/current.json'+'?'+'key=a078339df6874857856153714240111&'+f'q={loc.lower()}'
    else:
        current_weather_url = base_url + '/current.json'+'?'+'key=a078339df6874857856153714240111&'+"q=london"

    data = requests.get(current_weather_url)
    if data.status_code != 200:
        return "city not found"
    data = data.json()
    city = data.get('location').get('name')
    region = data.get('location').get('region')
    country = data.get('location').get('country')
    current_time = data.get('location').get('localtime')
    condition = data.get('current').get('condition').get('text')
    icon = data.get('current').get('condition').get('icon')
    wind = data.get('current').get('wind_kph')
    wind_dir = data.get('current').get('wind_dir')
    humidity = data.get('current').get('humidity')
    temperature = data.get('current').get('temp_c')
    rainfall = data.get('current').get('precip_mm')
    icon = 'https:'+icon 
    print(f'{city}{current_time}')
    return render_template('index.html',city=city,current_time=current_time, 
                            region=region,country=country,condition=condition,icon=icon,wind=wind,wind_dir=wind_dir, 
                            humidity=humidity,temperature=temperature,rainfall=rainfall)

@app.route("/suggestions",methods = ['GET','POST'])
def find_suggestions():
     loc = request.get_json()
     print("These prints are from suggestions")
     print(loc)
     search_weather_url = base_url + '/search.json'+'?'+'key=a078339df6874857856153714240111&'+f'q={loc.lower()}'
     search_data = requests.get(search_weather_url)
     return search_data.json()
     


if __name__ == '__main__':
    app.run(debug=True)