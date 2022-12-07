import os
import pprint
import requests
from dotenv import load_dotenv

pp = pprint.PrettyPrinter(indent=3)

load_dotenv()
token = os.getenv('SUPERJOB_SECRET_KEY')

# host = 'https://api.superjob.ru/2.0/vacancies/'
host = 'https://api.superjob.ru/2.0/catalogues/'
headers = {'X-Api-App-Id': token}
params = {
    'keyword': 'Программист',
    'count': 100,
    'page': 4
    }

# print(params)
response = requests.get(host, headers=headers, params=params)
response.raise_for_status()
'''
objects
total
more
subscription_id
subscription_active
'''

for x in response.json():
    True
    # print(x)


# pp.pprint(response.json()['objects'][0]['profession'])

print(*[f"{x['title_rus']}\n" for x in response.json()])
print(len(response.json()))

pp.pprint(response.json()[0])

# title: Разработка, программирование
# key: 48


# pp.pprint(response.json()['objects'][0])
# print(len(response.json()['objects']))
# 0_id: 34317966
