from pprint import pprint
from requests import get

url = 'https://digidon.herokuapp.com/'
token = 'yandex_lyceum_project'
login = 'x@a'

pprint(get(f'{url}/api/get_all_accounts&login={login}&token=greferfwe').json())

pprint(get(f'{url}/api/get_all_accounts&login={login}&token={token}').json())

pprint(get(f'{url}/api/get_one_account/4&login={login}&token={token}').json())

