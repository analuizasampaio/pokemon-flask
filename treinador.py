from flask import Flask, request, jsonify
from enum import Enum, auto
import jsons

treinadores = {}

class Genero(Enum):
    FEMININO = auto()
    MASCULINO = auto()

    @staticmethod
    def decodificar(valor):
        for g in Genero:
            if g.name.lower() == valor:
                return g
        raise ValueError()

    def __str__(self):
        return self.name.lower()

class PokemonJaExisteException(Exception):
    pass

class Treinador:
    def __init__(self, nome):
        self.__nome = nome
        self.__pokemons = {}

    @property
    def nome(self):
        return self.__nome

    @property
    def pokemons(self):
        return self.__pokemons

    def adicionar_pokemon(self, apelido, tipo, experiencia, genero):
        if apelido in self.__pokemons: raise PokemonJaExisteException()
        self.__pokemons[apelido] = Pokemon(apelido, tipo, experiencia, genero)

class Pokemon:
    def __init__(self, apelido, tipo, experiencia, genero):
        self.__apelido = apelido
        self.__tipo = tipo
        self.__genero = genero
        self.__experiencia = experiencia

    @property
    def apelido(self):
        return self.__apelido

    @property
    def tipo(self):
        return self.__tipo

    @property
    def experiencia(self):
        return self.__experiencia

    @property
    def genero(self):
        return self.__genero

    def ganhar_experiencia(self, ganho):
        self.__experiencia += ganho

def __enum_to_str(obj, **kwargs):
    return obj.__str__()

jsons.set_serializer(__enum_to_str, Enum)

def to_dict(obj):
    return jsons.dump(obj, strip_privates = True)

def to_dict_list(lista):
    resultado = []
    for item in lista:
        resultado.append(to_dict(item))
    return resultado

AUSENTE = {}

def validar_campos(obj, campos):

    def validar_campo(valor, tipo):
        if type(tipo) is type: return type(valor) is tipo
        if callable(type): return tipo(valor)
        raise ValueError()

    if type(campos) != dict:
        raise ValueError()
    if type(obj) != dict:
        return False
    for k in obj:
        if k not in campos:
            return False
    for k in campos:
        if k not in obj:
            valor = AUSENTE
        else:
            valor = obj[k]
        if not validar_campo(valor, campos[k]):
            return False
    return True

def opt(interno):
    def validador(valor):
        return valor is AUSENTE or interno(valor)
    return validador

def numerico(valor):
    return type(valor) in [int, float]

def natural(valor):
    return type(valor) is int and valor >= 0

def positivo(valor):
    return type(valor) in [int, float] and valor > 0

def int_positivo(valor):
    return type(valor) is int and valor > 0

def int_positivo_ou_zero(valor):
    return type(valor) is int and valor >= 0

def str_nao_vazio(valor):
    return type(valor) is str and valor != ''

status = {"closed": True}

# ROTAS DO FLASK DAQUI PARA BAIXO.

app = Flask(__name__)

@app.route("/hello")
def hello():
    return "Pikachu, eu escolho você!"

@app.route("/reset", methods = ["POST"])
def reset():
    status["closed"] = False
    treinadores.clear()
    return "Pikachu, eu escolho você!"

@app.route("/close", methods = ["POST"])
def close():
    status["closed"] = True
    treinadores.clear()
    return "Equipe Rocket decolando na velocidade da luz!"

@app.route("/treinador")
def listar_treinadores():
    if status["closed"]: return "Não use a API de treinadores agora.", 400
    return jsonify(to_dict(treinadores))

@app.route("/treinador/<nome>")
def detalhar_treinador(nome):
    if status["closed"]: return "Não use a API de treinadores agora.", 400
    if nome not in treinadores: return "", 404
    return jsonify(to_dict(treinadores[nome]))

@app.route("/treinador/<nome>/<apelido>")
def detalhar_pokemon(nome, apelido):
    if status["closed"]: return "Não use a API de treinadores agora.", 400
    if nome not in treinadores: return "Treinador não existe.", 404
    treinador = treinadores[nome]
    pokemons = treinador.pokemons
    if apelido not in pokemons: return "Pokémon não existe.", 404
    return jsonify(to_dict(pokemons[apelido]))

@app.route("/treinador/<nome>", methods = ["PUT"])
def cadastrar_treinador(nome):
    if status["closed"]: return "Não use a API de treinadores agora.", 400
    if nome in treinadores: return jsonify(to_dict(treinadores[nome])), 303
    t = Treinador(nome)
    treinadores[nome] = t
    return jsonify(to_dict(t)), 202

@app.route("/treinador/<nome>", methods = ["DELETE"])
def excluir_treinador(nome):
    if status["closed"]: return "Não use a API de treinadores agora.", 400
    if nome not in treinadores: return "", 404
    del treinadores[nome]
    return "", 204

def str_genero(valor):
    return valor in ['feminino', 'masculino']

@app.route("/treinador/<nome>/<apelido>", methods = ["PUT"])
def cadastrar_pokemon(nome, apelido):
    if status["closed"]: return "Não use a API de treinadores agora.", 400
    if nome not in treinadores: return "", 404
    treinador = treinadores[nome]
    pokemons = treinador.pokemons
    if apelido in pokemons: return "", 409
    dados = request.get_json()
    validar_campos(dados, {'tipo': str_nao_vazio, 'experiencia': natural, 'genero': str_genero})
    pokemon = treinador.adicionar_pokemon(apelido, dados['tipo'], dados['experiencia'], Genero.decodificar(dados['genero']))
    return jsonify(to_dict(pokemon)), 202

@app.route("/treinador/<nome>/<apelido>/exp", methods = ["POST"])
def adicionar_experiencia(nome, apelido):
    if status["closed"]: return "Não use a API de treinadores agora.", 400
    if nome not in treinadores: return "Treinador não existe.", 404
    treinador = treinadores[nome]
    pokemons = treinador.pokemons
    if apelido not in pokemons: return "Pokémon não existe.", 404
    pokemon = pokemons[apelido]
    dados = request.get_json()
    validar_campos(dados, {'experiencia': natural})
    pokemon.ganhar_experiencia(dados['experiencia'])
    return "", 204

@app.route("/treinador/<nome>/<apelido>", methods = ["DELETE"])
def excluir_pokemon(nome, apelido):
    if status["closed"]: return "Não use a API de treinadores agora.", 400
    if nome not in treinadores: return "Treinador não existe.", 404
    treinador = treinadores[nome]
    pokemons = treinador.pokemons
    if apelido not in pokemons: return "Pokémon não existe.", 404
    del pokemons[apelido]
    return "", 204

if __name__ == "__main__":
    app.run(port = 9000)