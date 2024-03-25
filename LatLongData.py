import requests


# Example 900 Boston Post Road, Guilford Center, CT, USA
# street num, street, city/town, state/province, country
class Geocode:
    def __init__(self, key):
        self.geocode_key = key
        self.url = url = f'https://api.geocodify.com/v2/geocode?api_key={self.geocode_key}'

    def get_long_lat(self, address):
        url2 = self.url + f'&q={address}'

        response = requests.get(url2)

        if response.status_code == 200:
            data = response.json()
            cords = data['response']['features'][0]['geometry']['coordinates'] # coordinates are in lat long convert
            return cords[1], cords[0]

        else:
            print(f"error: {response.status_code}")
            return
