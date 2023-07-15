from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/temperature', methods=['POST'])
def temperature():
    city = request.form.get('city')

    # Use Nominatim API to get latitude and longitude for the city
    geocoding_url = f'https://nominatim.openstreetmap.org/search?q={city}&format=json'
    geocoding_response = requests.get(geocoding_url)
    geocoding_data = geocoding_response.json()

    if geocoding_data:
        latitude = geocoding_data[0]['lat']
        longitude = geocoding_data[0]['lon']

        api_key = '00fe9ab9131e30b39b5d6f2ed53de144'  # Replace with your actual API key

        # Make API call to retrieve weather data using latitude and longitude
        
        url = f'https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}'
        response = requests.get(url)
        data = response.json()

        if data['cod'] == 200:
            temperature = data['main']['temp']
            humidity = data['main']['humidity']
            wind_speed = data['wind']['speed']
            weather_description = data['weather'][0]['description']
            return render_template('result.html', city=city, temperature=temperature, humidity=humidity,
                                   wind_speed=wind_speed, weather_description=weather_description)
        else:
            error_message = data['message']
            return render_template('error.html', error_message=error_message)
    else:
        error_message = "City not found"
        return render_template('error.html', error_message=error_message)

if __name__ == '__main__':
    app.run(debug=True)
