import pyowm
from pyowm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps

owm = pyowm.OWM('d1aff35b44e2555c08137cee836ba064')
mgr = owm.weather_manager()
user = input("Введите город: ")
observation = mgr.weather_at_place(user)
w = observation.weather

print(f"Статус погоды: {w.detailed_status}")
print(f"Температура: {w.temperature('celsius')['temp']}°C")
print(f"Скорость ветра: {w.wind()['speed']} м/с")
print(f"Влажность: {w.humidity}%")

print('hello')