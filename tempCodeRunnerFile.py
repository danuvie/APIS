import json
import requests 


URL = 'http://127.0.0.1:8081'

resposta_hoteis = requests.request('GET', URL, '/hoteis')

print(resposta_hoteis.statu_code)