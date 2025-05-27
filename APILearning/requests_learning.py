import requests
import json
# request.get(url)
# x = requests.get('https://w3schools.com/python/demopage.htm')
# print(x.text)
# x = requests.get('https://w3schools.com')
# # print(x.text)
# print(x.json)
# print(x.url)
# x = requests.get('https://www.w3schools.com/python/ref_requests_response.asp')
# # print(x.text)
# print(x.url)
# print(x.request)
# print(x.status_code)
# print(x.cookies.items)
# print(x.links)

y = requests.get('https://api.agify.io?name=michael')
print(y.json())
print(y.status_code)
print(y.text)
print(y.content)
print(y.json()["name"])
d = {'a': '1', 'b': True }
d = '{"a": "1", "b": true }'
var_json = json.dumps(d)
print(var_json)
var_json = json.loads(var_json)
print(var_json)