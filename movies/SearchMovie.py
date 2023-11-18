import requests

url = "https://movie-database-alternative.p.rapidapi.com/"

inpute = "Terminator"

querystring = {"s":inpute, "r":"json", "page":"1"}

headers = {
    "X-RapidAPI-Key": "081427815mshf6c0e29b9dd7964p1709b7j sn462710 f9959e",
    "X-RapidAPI-Host": "movie-database-alternative.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)
print(response.json)