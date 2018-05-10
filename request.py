import requests

endpoint = 'http://localhost:5000/api/test'

response = requests.get(endpoint)
print(response.json())
