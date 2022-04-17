import requests
numero = 42
site_pokeapi = "http://pokeapi.co"
limite = (4, 12)

resposta = requests.get(f"{site_pokeapi}/api/v2/pokemon/{numero}", timeout = limite)
j = resposta.json()
print(j["name"])