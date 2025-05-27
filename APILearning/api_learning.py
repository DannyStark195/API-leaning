import requests
import json
response = requests.get('http://api.stackexchange.com/2.2/questions?order=desc&sort=activity&site=stackoverflow')

for data in response.json()['items']:
    if data['is_answered'] == True:
        print(data['title'])
        print(data['link'])
    else:
        print(f'Skipped {data["title"]}')
    