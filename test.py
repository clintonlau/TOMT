import requests

BASE = "http://127.0.0.1:5000/"

data = [
    {"likes": 78, "name": "How to make API", "views": 81345},
    {"likes": 2, "name": "How to do this", "views": 124},
    {"likes": 82, "name": "How to do that", "views": 23461}
]

for i in range(len(data)):
    response = requests.put(BASE + "video/" + str(i), data[i])
    print(response.json())

input()
response = requests.get(BASE + "video/2")
print(response.json())