import requests
from django.http import JsonResponse

def fetch_kinopoisk_data(title):
    # kinopoisk_url = f'https://unogs-unogs-v1.p.rapidapi.com/search/titles={title}'
    # response = requests.get(kinopoisk_url)

    url = f'https://unogsng.p.rapidapi.com/search'
    headers = {
         'X-RapidAPI-Key': '46345d420amsh9c12bb9464d67e7p1c2d3djsnf9eec0f2df5c',
         'X-RapidAPI-Host': 'unogsng.p.rapidapi.com'
    }

    # Make the API request

       # Define the parameters for the search
    params = {
        'query': title,
        # Add other parameters as needed
    }

    response = requests.get(url, headers=headers, params=params)

    print('response', response.json())

    if response.status_code == 200:
        return response.json()
    else:
        return None
