import requests, os
from kivy.app import App
from kivy.lang import Builder
from dotenv import load_dotenv

load_dotenv()
#importing the api key from openweathermap.org
API_KEY = os.getenv("API_KEY")
#creating the class to pass to weather.kv
class WeatherApp(App):
    #creating the window
    def build(self):
        return Builder.load_file("weather.kv")
    #creating the function to get the weather on press of the button
    def get_weather(self):
        #stores the input from the search field
        city = self.root.ids.city_input.text.strip()
        #if there is no input
        if not city:
            self.root.ids.result_label.text = "Please enter a city"
            return
        #url of the city inputed in openweathermap.org
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

        try:
            self.root.ids.result_label.text = "Fetching weather..."
            response = requests.get(url)
            data = response.json()
            #if the city entered is not found
            if data.get("cod") != 200:
                self.root.ids.result_label.text = f"Error: {data.get('message','City not found')}"
            #if its found
            else:
                #store the first item in weather key from data and a description key
                weather = data["weather"][0]["description"]
                #store the temperature
                temp = data["main"]["temp"]
                #store the icon 
                icon_code = data["weather"][0]["icon"]
                icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
                #displaying the info
                self.root.ids.result_label.text = f"{city.title()}: {weather}, {temp}°C"
                self.root.ids.weather_icon.source = icon_url
        except Exception as e:
            self.root.ids.result_label.text = f"Error fetching weather: {e}"
    #get weather for specific cities on buttons
    def get_city_weather(self, city):
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        try:
            self.root.ids.result_label.text = "Fetching weather..."
            response = requests.get(url)
            data = response.json()
            icon_code = data["weather"][0]["icon"]
            icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
            if data.get("cod") != 200:
                self.root.ids.result_label.text = f"Error: {data.get("message", "City not found")}"
            else:
                weather = data["weather"][0]["description"]
                temp = data["main"]["temp"]
                self.root.ids.result_label.text = f"{city.title()}: {weather}, {temp}°C"
                self.root.ids.weather_icon.source = icon_url
        except Exception as e:
            self.root.ids.result_label.text = f"Error fetching weather: {e}"

if __name__ == "__main__":
    WeatherApp().run()