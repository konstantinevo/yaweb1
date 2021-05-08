
import requests


def image(address):
    a1 = '+'.join(address.split())
    geocoder_request = f'http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&format' \
                       f'=json&geocode={a1}'
    response = requests.get(geocoder_request)

    if response:
        json_response = response.json()
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        toponym_coodrinates = toponym["Point"]["pos"]
        addr = toponym_coodrinates.split()

        map_request = f'https://static-maps.yandex.ru/1.x/?ll={addr[0]},{addr[-1]}&spn=0.002,0.002&l=map&pt={addr[0]},{addr[-1]},pmwtm1~{addr[0]},{addr[-1]}'
        response = requests.get(map_request)

        map_file = f'static/img/map1.png'
        with open(map_file, "wb") as file:
            file.write(response.content)