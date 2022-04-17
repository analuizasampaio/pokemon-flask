import requests
from dataclasses import dataclass
from enum import Enum, auto

"""
Instruções para TODOS os exercícios/funções abaixo:

1. Para executar os testes, execute "python treinador.py" e paralelamente a isso, "python pokemon_unittest.py".

2. None e strings em branco são sempre consideradas inválidas quando utilizadas como parâmetros.

3. Não se preocupe com erros de tipo (como por exemplo, passar uma string para uma função que trabalha com números). Esse tipo de coisa não está nos testes.

4. Todos os nomes de pokémons nos testes estão em letras minúsculas.
   Entretanto, se você quiser aceitar MAIÚSCULAS ou até mesmo mIsTuRaDo, aplicando uma chamada à lower() ou coisa semelhante, isso fica a seu critério.
   Os testes não verificam diferenças de maiúsculas/minúsculas.

5. Desconsiderando-se os erros de tipo, se algum parâmetro puder ser determinado como inválido antes que alguma chamada a um servidor externo seja realizada, então ele deve ser detectado como tal sem que o servidor seja contactado, mesmo se ele estiver off-line.

6. Em todos os casos onde procura-se algum tipo de pokémon pelo nome ou pelo número e o mesmo não existir, uma exceção PokemonNaoExisteException deve ser lançada.

7. Em todos os casos onde procura-se algum treinador cadastrado e o mesmo não existir, uma exceção TreinadorNaoCadastradoException deve ser lançada.

8. Em todos os casos onde procura-se algum pokémon pertencente a algum treinador e o mesmo não existir, uma exceção PokemonNaoCadastradoException deve ser lançada.

9. Em todos os casos onde tenta-se cadastrar um pokémon e o mesmo já exista, uma exceção PokemonJaCadastradoException deve ser lançada.

10. Todos os nomes de pokémons, cores, jogos, movimentos, etc. recebidos e devolvidos pela PokéAPI estão em letras minúsculas e assim devem ser mantidas.

11. Consulte a documentação em (https://pokeapi.co/docs/v2.html).

12. Não se esqueça de configurar o arquivo config.json para que o script dos testes possa encontrar os servidores locais da PokéAPI e também do treinador.

13. A API do treinador não tem documentação! Para entender como usá-la, olhe o código e tente deduzir.

14. Seguem alguns exemplos de URLs que podem servir para te ajudar:
    https://pokeapi.co/api/v2/
    https://pokeapi.co/api/v2/pokemon/39/
    https://pokeapi.co/api/v2/pokemon/jigglypuff/
    https://pokeapi.co/api/v2/pokemon-species/39/
    https://pokeapi.co/api/v2/pokemon-species/jigglypuff/
    https://pokeapi.co/api/v2/evolution-chain/11/
    https://pokeapi.co/api/v2/growth-rate/1/
    https://pokeapi.co/api/v2/pokemon-color/2/
"""

"""
Não altere estas URLs. Elas são utilizadas para conectar no treinador e no PokéAPI, respectivamente.
"""
site_treinador = "http://127.0.0.1:9000"
site_pokeapi = "http://pokeapi.co"

"""
Use isso como parâmetro "timeout" em todas as chamadas ao requests.
Por exemplo:
    requests.get(f"{site_pokeapi}/api/v2/", timeout = limite)
"""
limite = (4, 12)

"""
Vamos precisar destas quatro exceções. Não altere o código delas.
"""
class PokemonNaoExisteException(Exception):
    pass

class PokemonNaoCadastradoException(Exception):
    pass

class TreinadorNaoCadastradoException(Exception):
    pass

class PokemonJaCadastradoException(Exception):
    pass

"""
1. Dado o número de um pokémon, qual é o nome dele?

Observações:
- Presuma que nunca irá existir mais do que 5000 pokémons diferentes.
- Também não existe pokémon de número zero ou negativo.
- Assim sendo, nem precisa fazer a requisição nesses casos.
- Se o pokémon não existir, lance uma PokemonNaoExisteException.
"""
def nome_do_pokemon(numero):
    raise Exception("Não implementado.")

"""
2. Dado o nome de um pokémon, qual é o número dele?

Observações:
- Não se esqueça de verificar os casos onde o pokémon procurado não exista (PokemonNaoExisteException).
"""
def numero_do_pokemon(nome):
    raise Exception("Não implementado.")

"""
3. Dado o nome de um pokémon, qual é o nome da cor (em inglês) predominante dele?

Observações:
- Não se esqueça de verificar os casos onde o pokémon procurado não exista.
"""
def color_of_pokemon(nome):
    raise Exception("Não implementado.")

"""
4. Dado o nome de um pokémon, qual é o nome da cor (em português) predominante dele?

Observações:
- Os nomes de cores possíveis de pokémons em português são APENAS as "marrom", "amarelo", "azul", "rosa", "cinza", "roxo", "vermelho", "branco", "verde" e "preto".
- No entanto, a pokeapi ainda não foi traduzida para o português! Como você pode dar um jeito nisso?

Dicas:
- O que os dicionários do python e os dicionários que você compra em livrarias têm em comum além do nome?
- Faça uma invocação à função color_of_pokemon acima.
"""
def cor_do_pokemon(nome):
    raise Exception("Não implementado.")

"""
5. Dado o nome de um pokémon, quais são os tipos no qual ele se enquadra?
Os nomes dos tipos de pokémons em português são "normal", "lutador", "voador", "veneno", "terra", "pedra", "inseto", "fantasma", "aço", "fogo", "água", "grama", "elétrico", "psíquico", "gelo", "dragão", "noturno" e "fada".
Todo pokémon pode pertencer a um ou a dois tipos diferentes. Retorne uma lista (ou um set ou uma tupla ou coisa similar, se preferir) contendo os tipos, mesmo que haja somente um.
Se houver dois tipos, a ordem não é importante.

Observações:
- Não se esqueça de verificar os casos onde o pokémon procurado não exista.
"""
def tipos_do_pokemon(nome):
    raise Exception("Não implementado.")

"""
6. Dado o nome de um pokémon, liste de qual pokémon ele evoluiu.
Por exemplo, evolucao_anterior('venusaur') == 'ivysaur'
Retorne None se o pokémon não tem evolução anterior. Por exemplo, evolucao_anterior('bulbasaur') == None

Observações:
- Não se esqueça de verificar os casos onde o pokémon procurado não exista.
"""
def evolucao_anterior(nome):
    raise Exception("Não implementado.")

"""
7. Dado o nome de um pokémon, liste para quais pokémons ele pode evoluiur.
Por exemplo, evolucoes_proximas('ivysaur') == ['venusaur'].
A maioria dos pokémons que podem evoluir, só podem evoluir para um único tipo de pokémon próximo. No entanto, há alguns que podem evoluir para dois ou mais tipos diferentes de pokémons.
Se houver múltiplas possibilidades de evoluções, a ordem delas não importa. Por exemplo:
evolucoes_proximas('poliwhirl') == ['poliwrath', 'politoed']
Note que esta função dá como resultado somente o próximo passo evolutivo. Assim sendo, evolucoes_proximas('poliwag') == ['poliwhirl']
Se o pokémon não evolui, retorne uma lista vazia. Por exemplo, evolucoes_proximas('celebi') == []

Observações:
- Não se esqueça de verificar os casos onde o pokémon procurado não exista.

Dicas:
- Possivelmente o JSON que a API irá te devolver será algo bem complicado de analisar.
- Possivelmente você terá que fazer 2 ou mais requisições aqui.
- Uma forma de resolver este exercício inclui utilizar recursão.
"""
def evolucoes_proximas(nome):
    raise Exception("Não implementado.")

"""
8. A medida que ganham pontos de experiência, os pokémons sobem de nível.
É possível determinar o nível (1 a 100) em que um pokémon se encontra com base na quantidade de pontos de experiência que ele tem.
Entretanto, cada tipo de pokémon adota uma curva de level-up diferente (na verdade, existem apenas 6 curvas de level-up diferentes).
Assim sendo, dado um nome de pokémon e uma quantidade de pontos de experiência, retorne o nível em que este pokémon está.
Valores negativos de experiência devem ser considerados inválidos.

Observações:
- Não se esqueça de verificar os casos onde o pokémon procurado não exista.
- Lance uma exceção ValueError para os casos onde o valor da experiência é negativo.
- Não realize os cálculos diretamente nesta função implementando nela alguma fórmula matemática. Utilize a API para fazer os cálculos.
"""
def nivel_do_pokemon(nome, experiencia):
    raise Exception("Não implementado.")

"""
Até agora, temos representado as espécies de pokemóns apenas como uma string, no entanto podemos representá-los com uma classe.
Esta classe representa uma espécie de pokémon, e cada instância carrega dentro de si o nome de uma espécie de pokémon, a cor e as informações da evolução.
"""
@dataclass(frozen = True)
class EspeciePokemon:
    nome: str
    cor: str
    evoluiu_de: str
    evolui_para: list

    """
    9. Com base nas funções acimas, implemente o método estático por_nome da classe EspeciePokemon.
    Esse método deve retornar uma instância de EspeciePokemon contendo o nome da espécie, a cor e as informações sobre a evolução.
    """
    @staticmethod
    def por_nome(nome):
        raise Exception("Não implementado.")

"""
10. Dado um nome de treinador, cadastre-o na API de treinador.
Retorne True se um treinador com esse nome foi criado e False em caso contrário (já existia).
"""
def cadastrar_treinador(nome):
    raise Exception("Não implementado.")

"""
Vamos precisar desta classe logo abaixo.
"""
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

"""
Agora, nós implementaremos alguns métodos desta classe (Pokemon). Não deve-se confundí-la com EspeciePokemon.
Vamos supor que você tenha dois pokémons da espécie Ponyta. Para diferenciá-los, decida chamar um de "veloz" e o outro de "ligeirinho".
Seu amigo também tem uma Ponyta, que ele chama de "quentinha".
Nesse caso, "veloz", "ligeirinho" e "quentinha" são três Ponytas diferentes, pertencentes a dois treinadores diferentes.
Além disso, esses diferentes pokémons, embora da mesma espécie, também podem ser de sexos diferentes e com diferentes quantidades de pontos de experiência.
"""
class Pokemon:

    def __init__(self, nome_treinador, apelido, tipo, experiencia, genero):
        if experiencia < 0: raise ValueError()
        self.__nome_treinador = nome_treinador
        self.__apelido = apelido
        self.__tipo = tipo
        self.__experiencia = experiencia
        self.__genero = genero

    @property
    def nome_treinador(self):
        return self.__nome_treinador

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

    """
    11. Você consegue definir uma implementação para essa propriedade?
    Dica:
    - Você pode usar a função nivel_do_pokemon definida acima:
    """
    @property
    def nivel(self):
        raise Exception("Não implementado.")

    """
    12. Imagine que você capturou dois pokémons do mesmo tipo. Para diferenciá-los, você dá nomes diferentes (apelidos) para eles.
    Logo, um treinador pode ter mais do que um pokémon de um determinado tipo, mas não pode ter dois pokémons diferentes com o mesmo apelido.
    Assim sendo, dado um nome de treinador, um apelido de pokémon, um tipo de pokémon e uma quantidade de experiência, cadastre o pokémon com o tipo correspondente ao treinador dado na API do treinador.
    Certifique-se de que todos os dados são válidos.
    """
    def cadastrar(self):
        raise Exception("Não implementado.")

    """
    13. Dado um pokémon (o que é representado pelo self) acrescente-lhe a experiência ganha na API do treinador (e no própria instância também).
    
    Observação:
    - A experiêcia ganha não pode ser um número negativo. Lance um ValueError nesse caso.
    """
    def ganhar_experiencia(self, ganho):
        raise Exception("Não implementado.")

    """
    14. Dado um nome de treinador e um apelido de pokémon, localize esse pokémon na API do treinador.
        A API do treinador trará como resultado, a espécie do pokémon, a quantidade de experiência que ele tem e o seu gênero.
        Finalmente, este método deve retornar um objeto que seja uma instância da classe Pokemon.
    """
    @staticmethod
    def localizar_pokemon(nome_treinador, apelido_pokemon):
        raise Exception("Não implementado.")

"""
15 Dado o nome de um treinador, localize-o na API do treinador e retorne um dicionário contendo como chaves, os apelidos de seus pokémons e como valores os nomes dos tipos deles.
"""
def detalhar_treinador(nome_treinador):
    raise Exception("Não implementado.")

"""
16. Dado o nome de um treinador, localize-o na API do treinador e exclua-o, juntamente com todos os seus pokémons.
"""
def excluir_treinador(nome_treinador):
    raise Exception("Não implementado.")

"""
17. Dado o nome de um treinador e o apelido de um de seus pokémons, localize o pokémon na API do treinador e exclua-o.
"""
def excluir_pokemon(nome_treinador, apelido_pokemon):
    raise Exception("Não implementado.")