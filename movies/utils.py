import requests

def fetch_kinopoisk_data(title):
    kinopoisk_url = f'https://api.kinopoisk.dev/movie?title={title}'
    response = requests.get(kinopoisk_url)

    if response.status_code == 200:
        return response.json()
    else:
        return None
