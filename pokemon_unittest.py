import unittest
import requests
from pokemon import *

parar_no_primeiro_erro = False

ultimo_pokemon = 898

from functools import wraps

def verificar_erro(interno, tipo_erro, tests = None):
    if tests is None:
        try:
            interno()
        except Exception as x:
            assert type(x) is tipo_erro, f"Esperava-se que um erro do tipo {tipo_erro.__name__}, mas obteve-se uma do tipo {x.__class__.__name__}."
        else:
            assert False, f"Esperava-se que um erro do tipo {tipo_erro.__name__} fosse produzido, mas não foi."
    else:
        try:
            interno()
        except Exception as x:
            tests.assertIs(type(x), tipo_erro, f"Esperava-se que um erro do tipo {tipo_erro.__name__}, mas obteve-se uma do tipo {x.__class__.__name__}.")
        else:
            tests.fail(f"Esperava-se que um erro do tipo {tipo_erro.__name__} fosse produzido, mas não foi.")

def pokemon_nao_existe(interno, tests = None):
    verificar_erro(interno, PokemonNaoExisteException, tests)

def pokemon_nao_cadastrado(interno, tests = None):
    verificar_erro(interno, PokemonNaoCadastradoException, tests)

def treinador_nao_cadastrado(interno, tests = None):
    verificar_erro(interno, TreinadorNaoCadastradoException, tests)

def pokemon_ja_cadastrado(interno, tests = None):
    verificar_erro(interno, PokemonJaCadastradoException, tests)

def valor_errado(interno, tests = None):
    verificar_erro(interno, ValueError, tests)

def qualquer_erro(interno, tests = None):
    try:
        interno()
    except Exception as x:
        pass
    else:
        if tests is None:
            assert False, f"Esperava-se que um erro fosse produzido, mas não foi."
        else:
            tests.fail(f"Esperava-se que um erro fosse produzido, mas não foi.")

def assert_equals_unordered_list(esperada, obtida, tests = None):
    if tests is None:
        assert len(esperada) == len(obtida), f"Esperava-se que o resultado fosse {obtida}, mas foi {esperada}."
        for item in esperada:
            assert item in obtida, f"Esperava-se que o resultado fosse {obtida}, mas foi {esperada}."
    else:
        tests.assertEqual(len(esperada), len(obtida), f"Esperava-se que o resultado fosse {obtida}, mas foi {esperada}.")
        for item in esperada:
            tests.assertIn(item, obtida, f"Esperava-se que o resultado fosse {obtida}, mas foi {esperada}.")

class NoStdIO:
    def __init__(self):
        import sys
        self.__oout = sys.stdout
        self.__oin = sys.stdin
        self.__usou_print = False
        self.__usou_input = False
        self.__privilegio = False

    def __enter__(self):
        import sys
        self.__oout = sys.stdout
        self.__oin = sys.stdin
        sys.stdout = self
        sys.stdin = self

    def __exit__(self, a, b, c):
        import sys
        sys.stdout = self.__oout
        sys.stdin = self.__oin

    def write(self, t):
        if not self.__privilegio:
            self.__usou_print = True
        return self.__oout.write(t)

    def print_privilegiado(self, texto):
        self.__privilegio = True
        try:
            print(texto)
        finally:
            self.__privilegio = False

    def readline(self):
        self.__usou_input = True
        return self.__oin.readline()

    def flush(self):
        pass

    def __call__(self, delegate):
        @wraps(delegate)
        def sem_input(*args, **kwargs):
            with self:
                return delegate(*args, **kwargs)
        return sem_input

    def test_print(self):
        if self.__usou_print: raise Exception("Você não deveria utilizar a função print neste exercício.")

    def test_input(self):
        if self.__usou_input: raise Exception("Você não deveria utilizar a função input neste exercício.")

sem_io = NoStdIO()

class ContaPontos:
    def __init__(self):
        self.__total = 0
        self.__acumulado = 0
        self.__map = {}

    def prepare(self, grupo, qtd, penalidade, after_fail):
        if grupo != 'Bônus': self.__total += qtd
        if grupo in self.__map:
            self.__map[grupo]['total'] += qtd
        else:
            self.__map[grupo] = {'total': qtd, 'executado': 0, 'penalidade': 0}

        def intermediaria(interna):
            @wraps(interna)
            def contando(*args, **kwargs):
                try:
                    with sem_io:
                        x = interna(*args, **kwargs)
                    self.__acumulado += qtd
                    self.__map[grupo]['executado'] += qtd
                    return x
                except Exception as z:
                    self.__map[grupo]['penalidade'] -= penalidade
                    self.__acumulado -= penalidade
                    after_fail(z)
                    raise z
            return contando
        return intermediaria

    def mostrar_pontos(self):
        if self.__total == 0:
            print("Os testes não foram executados.")
            return
        pontos = max(0, min(10, self.__acumulado * 10 / self.__total))
        def arredondar(v):
            s = f"X{v:4.2f}Y".replace(".", ",")
            while s.find("0Y") != -1: s = s.replace("0Y", "Y")
            return s.replace(",Y", "Y").replace("XY", "X0Y")[1:-1]
        ps = arredondar(pontos)
        print(f"Sua pontuação é de {self.__acumulado} / {self.__total}. Logo, sua nota é {ps}.")
        for valor in sorted(self.__map.keys()):
            t = self.__map[valor]['total']
            e = self.__map[valor]['executado']
            p = self.__map[valor]['penalidade']
            if t == 0 and p == 0:
                print(f'- O quesito "{valor}" está ok.')
            elif t == 0:
                print(f'- No quesito "{valor}", houve uma PENALIDADE de {p}.')
            elif p == 0:
                print(f'- No quesito "{valor}", sua pontuação é de {e} / {t}.')
            else:
                print(f'- No quesito "{valor}", sua pontuação é de {e} / {t}, mas houve uma PENALIDADE de {p}, totalizando {(e - p)} / {t}.')

pontos_main = ContaPontos()

def teste_erro():
    raise Exception("Não rodou no teste anterior.")

bonus_check = teste_erro

def teste(grupo, qtd, penalidade = 0):
    return pontos_main.prepare(grupo, qtd, penalidade, sem_io.print_privilegiado)

# Pokémons utilizados como massa de teste.
charizard = EspeciePokemon("charizard", "vermelho", "charmeleon", [])
pidgeotto = EspeciePokemon("pidgeotto", "marrom", "pidgey", ["pidgeot"])
pikachu = EspeciePokemon("pikachu", "amarelo", "pichu", ["raichu"])
raikou = EspeciePokemon("raikou", "amarelo", None, [])
gloom = EspeciePokemon("gloom", "azul", "oddish", ["vileplume", "bellossom"])
koffing = EspeciePokemon("koffing", "roxo", None, ["weezing"])
weezing = EspeciePokemon("weezing", "roxo", "koffing", [])
weepinbell = EspeciePokemon("weepinbell", "verde", "bellsprout", ["victreebel"])
victreebel = EspeciePokemon("victreebel", "verde", "weepinbell", [])
wobbuffet = EspeciePokemon("wobbuffet", "azul", "wynaut", [])
arbok = EspeciePokemon("arbok", "roxo", "ekans", [])
lickitung = EspeciePokemon("lickitung", "rosa", "lickilicky", [])
magikarp = EspeciePokemon("magikarp", "vermelho", None, ["gyarados"])
staryu = EspeciePokemon("staryu", "marrom", None, ["starmie"])
geodude = EspeciePokemon("geodude", "marrom", None, ["graveler"])
onix = EspeciePokemon("onix", "cinza", None, ["steelix"])

class TestPokemon(unittest.TestCase):

    def reset(self):
        resposta = requests.post(f"{site_treinador}/reset", timeout = limite)
        self.assertEqual(resposta.status_code, 200)

    def close(self):
        resposta = requests.post(f"{site_treinador}/close", timeout = limite)
        self.assertEqual(resposta.status_code, 200)

    @teste("Não mexeu onde não deveria", 0, penalidade = 20)
    def test_00a_genero_ok(self):
        if len(Genero) != 2 or Genero.MASCULINO == Genero.FEMININO or str(Genero.MASCULINO) != "masculino" or str(Genero.FEMININO) != "feminino":
            raise Exception("Você bagunçou com a classe Genero.")

    @teste("Não mexeu onde não deveria", 0, penalidade = 20)
    def test_00b_especie_pokemon_ok(self):
        self.assertEqual(pidgeotto.nome, "pidgeotto")
        self.assertEqual(pidgeotto.cor, "marrom")
        self.assertEqual(pidgeotto.evoluiu_de, "pidgey")
        self.assertEqual(pidgeotto.evolui_para, ["pidgeot"])

    @teste("Não mexeu onde não deveria", 0, penalidade = 20)
    def test_00c_especie_pokemon_imutavel(self):
        def xxx1(): pidgeotto.nome = "dollynho"
        def xxx2(): pidgeotto.cor = "verde"
        def xxx3(): pidgeotto.evoluiu_de = "sua mãe"
        def xxx4(): pidgeotto.evolui_para = ["seu pai"]
        qualquer_erro(xxx1, self)
        qualquer_erro(xxx2, self)
        qualquer_erro(xxx3, self)
        qualquer_erro(xxx4, self)
        self.assertEqual(pidgeotto.nome, "pidgeotto")
        self.assertEqual(pidgeotto.cor, "marrom")
        self.assertEqual(pidgeotto.evoluiu_de, "pidgey")
        self.assertEqual(pidgeotto.evolui_para, ["pidgeot"])

    @teste("Não mexeu onde não deveria", 0, penalidade = 30)
    def test_00d_pokemon_ok(self):
        pq = Pokemon("Homer Simpson", "Bart", pikachu, 50000, Genero.MASCULINO)
        self.assertEqual(pq.nome_treinador, "Homer Simpson")
        self.assertEqual(pq.apelido, "Bart")
        self.assertEqual(pq.tipo, pikachu)
        self.assertEqual(pq.experiencia, 50000)
        self.assertEqual(pq.genero, Genero.MASCULINO)

    @teste("Não mexeu onde não deveria", 0, penalidade = 30)
    def test_00e_pokemon_imutavel(self):
        pq = Pokemon("Homer Simpson", "Bart", pikachu, 50000, Genero.MASCULINO)
        def xxx1(): pq.nome_treinador = "Margie Simpson"
        def xxx2(): pq.apelido = "Lisa"
        def xxx3(): pq.tipo = raikou
        def xxx4(): pq.experiencia = 6666
        def xxx5(): pq.genero = Genero.FEMININO
        qualquer_erro(xxx1, self)
        qualquer_erro(xxx2, self)
        qualquer_erro(xxx3, self)
        qualquer_erro(xxx4, self)
        qualquer_erro(xxx5, self)
        self.assertEqual(pq.nome_treinador, "Homer Simpson")
        self.assertEqual(pq.apelido, "Bart")
        self.assertEqual(pq.tipo, pikachu)
        self.assertEqual(pq.experiencia, 50000)
        self.assertEqual(pq.genero, Genero.MASCULINO)

    @teste("Não mexeu onde não deveria", 0, penalidade = 20)
    def test_00f_excecoes_ok(self):
        self.assertTrue(isinstance(PokemonNaoExisteException(), Exception))
        self.assertTrue(isinstance(PokemonNaoCadastradoException(), Exception))
        self.assertTrue(isinstance(TreinadorNaoCadastradoException(), Exception))
        self.assertTrue(isinstance(PokemonJaCadastradoException(), Exception))

    @teste("Exercício 01", 8)
    def test_01a_ok(self):
        self.close()
        self.assertEqual(nome_do_pokemon(  1), "bulbasaur")
        self.assertEqual(nome_do_pokemon( 55), "golduck")
        self.assertEqual(nome_do_pokemon( 25), "pikachu")
        self.assertEqual(nome_do_pokemon(700), "sylveon")
        self.assertEqual(nome_do_pokemon(807), "zeraora")
        nome_do_pokemon(ultimo_pokemon)

    @teste("Exercício 01", 1)
    def test_01b_numero_grande_demais(self):
        self.close()
        pokemon_nao_existe(lambda : nome_do_pokemon(ultimo_pokemon + 1), self)
        pokemon_nao_existe(lambda : nome_do_pokemon(4999), self)

    @teste("Exercício 01", 1)
    def test_01c_nao_existe(self):
        self.close()
        pokemon_nao_existe(lambda : nome_do_pokemon(   0), self)
        pokemon_nao_existe(lambda : nome_do_pokemon(  -1), self)
        pokemon_nao_existe(lambda : nome_do_pokemon(  -2), self)
        pokemon_nao_existe(lambda : nome_do_pokemon(-666), self)
        pokemon_nao_existe(lambda : nome_do_pokemon(5000), self)

    @teste("Exercício 01", 1)
    def test_01d_nao_existe_pegadinha(self):
        self.close()
        pokemon_nao_existe(lambda : nome_do_pokemon(10001), self)

    @teste("Exercício 02", 10)
    def test_02a_ok(self):
        self.close()
        self.assertEqual(numero_do_pokemon("marill"), 183)
        self.assertEqual(numero_do_pokemon("eevee"), 133)
        self.assertEqual(numero_do_pokemon("psyduck"), 54)
        self.assertEqual(numero_do_pokemon("skitty"), 300)
        self.assertEqual(numero_do_pokemon("zeraora"), 807)

    @teste("Exercício 02", 1)
    def test_02b_nao_existe(self):
        self.close()
        pokemon_nao_existe(lambda : numero_do_pokemon("dollynho"), self)
        pokemon_nao_existe(lambda : numero_do_pokemon("dobby"), self)
        pokemon_nao_existe(lambda : numero_do_pokemon("peppa-pig"), self)
        pokemon_nao_existe(lambda : numero_do_pokemon("batman"), self)
        pokemon_nao_existe(lambda : numero_do_pokemon("spiderman"), self)

    @teste("Exercício 02", 1)
    def test_02c_vazio(self):
        self.close()
        pokemon_nao_existe(lambda : numero_do_pokemon(""), self)

    @teste("Exercício 03", 7)
    def test_03a_ok(self):
        self.close()
        self.assertEqual(color_of_pokemon("marill"), "blue")
        self.assertEqual(color_of_pokemon("togekiss"), "white")
        self.assertEqual(color_of_pokemon("magneton"), "gray")
        self.assertEqual(color_of_pokemon("eevee"), "brown")
        self.assertEqual(color_of_pokemon("psyduck"), "yellow")
        self.assertEqual(color_of_pokemon("skitty"), "pink")
        self.assertEqual(color_of_pokemon("gastly"), "purple")
        self.assertEqual(color_of_pokemon("ledyba"), "red")
        self.assertEqual(color_of_pokemon("torterra"), "green")
        self.assertEqual(color_of_pokemon("xurkitree"), "black")

    @teste("Exercício 03", 2)
    def test_03b_nao_existe(self):
        self.close()
        pokemon_nao_existe(lambda : color_of_pokemon("dollynho"), self)
        pokemon_nao_existe(lambda : color_of_pokemon("dobby"), self)
        pokemon_nao_existe(lambda : color_of_pokemon("peppa-pig"), self)
        pokemon_nao_existe(lambda : color_of_pokemon("batman"), self)
        pokemon_nao_existe(lambda : color_of_pokemon("spiderman"), self)

    @teste("Exercício 03", 1)
    def test_03c_vazio(self):
        self.close()
        pokemon_nao_existe(lambda : color_of_pokemon(""), self)

    @teste("Exercício 04", 7)
    def test_04a_ok(self):
        self.close()
        self.assertEqual(cor_do_pokemon("marill"), "azul")
        self.assertEqual(cor_do_pokemon("togekiss"), "branco")
        self.assertEqual(cor_do_pokemon("magneton"), "cinza")
        self.assertEqual(cor_do_pokemon("eevee"), "marrom")
        self.assertEqual(cor_do_pokemon("psyduck"), "amarelo")
        self.assertEqual(cor_do_pokemon("skitty"), "rosa")
        self.assertEqual(cor_do_pokemon("gastly"), "roxo")
        self.assertEqual(cor_do_pokemon("ledyba"), "vermelho")
        self.assertEqual(cor_do_pokemon("torterra"), "verde")
        self.assertEqual(cor_do_pokemon("xurkitree"), "preto")

    @teste("Exercício 04", 2)
    def test_04b_nao_existe(self):
        self.close()
        pokemon_nao_existe(lambda : cor_do_pokemon("dollynho"), self)
        pokemon_nao_existe(lambda : cor_do_pokemon("dobby"), self)
        pokemon_nao_existe(lambda : cor_do_pokemon("peppa-pig"), self)
        pokemon_nao_existe(lambda : cor_do_pokemon("batman"), self)
        pokemon_nao_existe(lambda : cor_do_pokemon("spiderman"), self)

    @teste("Exercício 04", 1)
    def test_04c_vazio(self):
        self.close()
        pokemon_nao_existe(lambda : cor_do_pokemon(""), self)

    @teste("Exercício 05", 10)
    def test_05a_ok(self):
        self.close()
        assert_equals_unordered_list(["grama"], tipos_do_pokemon("chikorita"), self)
        assert_equals_unordered_list(["terra"], tipos_do_pokemon("hippowdon"), self)
        assert_equals_unordered_list(["normal", "fada"], tipos_do_pokemon("jigglypuff"), self)
        assert_equals_unordered_list(["fogo"], tipos_do_pokemon("darumaka"), self)
        assert_equals_unordered_list(["pedra", "voador"], tipos_do_pokemon("archeops"), self)
        assert_equals_unordered_list(["água"], tipos_do_pokemon("feebas"), self)
        assert_equals_unordered_list(["voador", "noturno"], tipos_do_pokemon("murkrow"), self)
        assert_equals_unordered_list(["água", "elétrico"], tipos_do_pokemon("chinchou"), self)
        assert_equals_unordered_list(["lutador", "fantasma"], tipos_do_pokemon("marshadow"), self)
        assert_equals_unordered_list(["aço"], tipos_do_pokemon("klink"), self)
        assert_equals_unordered_list(["lutador", "inseto"], tipos_do_pokemon("heracross"), self)
        assert_equals_unordered_list(["veneno", "noturno"], tipos_do_pokemon("drapion"), self)
        assert_equals_unordered_list(["psíquico", "gelo"], tipos_do_pokemon("jynx"), self)
        assert_equals_unordered_list(["dragão"], tipos_do_pokemon("dratini"), self)

    @teste("Exercício 05", 1)
    def test_05b_nao_existe(self):
        self.close()
        pokemon_nao_existe(lambda : tipos_do_pokemon("dollynho"), self)
        pokemon_nao_existe(lambda : tipos_do_pokemon("dobby"), self)
        pokemon_nao_existe(lambda : tipos_do_pokemon("peppa-pig"), self)
        pokemon_nao_existe(lambda : tipos_do_pokemon("batman"), self)
        pokemon_nao_existe(lambda : tipos_do_pokemon("spiderman"), self)

    @teste("Exercício 05", 1)
    def test_05c_vazio(self):
        self.close()
        pokemon_nao_existe(lambda : tipos_do_pokemon(""), self)

    @teste("Exercício 06", 7)
    def test_06a_ok(self):
        self.close()
        self.assertEqual(evolucao_anterior("togetic"), "togepi")
        self.assertEqual(evolucao_anterior("togekiss"), "togetic")
        self.assertEqual(evolucao_anterior("eelektrik"), "tynamo")
        self.assertEqual(evolucao_anterior("eelektross"), "eelektrik")
        self.assertEqual(evolucao_anterior("pikachu"), "pichu")
        self.assertEqual(evolucao_anterior("raichu"), "pikachu")

    @teste("Exercício 06", 2)
    def test_06b_nao_tem(self):
        self.close()
        self.assertIs(evolucao_anterior("togepi"), None)
        self.assertIs(evolucao_anterior("tynamo"), None)
        self.assertIs(evolucao_anterior("pichu"), None)

    @teste("Exercício 06", 1)
    def test_06c_nao_existe(self):
        self.close()
        pokemon_nao_existe(lambda : evolucao_anterior("dollynho"), self)
        pokemon_nao_existe(lambda : evolucao_anterior("dobby"), self)
        pokemon_nao_existe(lambda : evolucao_anterior("peppa-pig"), self)
        pokemon_nao_existe(lambda : evolucao_anterior("batman"), self)
        pokemon_nao_existe(lambda : evolucao_anterior("spiderman"), self)

    @teste("Exercício 06", 1)
    def test_06d_vazio(self):
        self.close()
        pokemon_nao_existe(lambda : evolucao_anterior(""), self)

    @teste("Exercício 07", 4)
    def test_07a_ok_evolucoes_simples(self):
        self.close()
        assert_equals_unordered_list(["charmeleon"], evolucoes_proximas("charmander"), self)
        assert_equals_unordered_list(["combusken"], evolucoes_proximas("torchic"), self)
        assert_equals_unordered_list(["charizard"], evolucoes_proximas("charmeleon"), self)

    @teste("Exercício 07", 1)
    def test_07b_ok_nao_tem_simples(self):
        self.close()
        assert_equals_unordered_list([], evolucoes_proximas("lugia"), self)
        assert_equals_unordered_list([], evolucoes_proximas("turtonator"), self)
        assert_equals_unordered_list([], evolucoes_proximas("charizard"), self)
        assert_equals_unordered_list([], evolucoes_proximas("gengar"), self)
        assert_equals_unordered_list([], evolucoes_proximas("alakazam"), self)

    @teste("Exercício 07", 4)
    def test_07c_ok_evolucoes_complexas(self):
        self.close()
        assert_equals_unordered_list(["ninjask", "shedinja"], evolucoes_proximas("nincada"), self)
        assert_equals_unordered_list(["vaporeon", "jolteon", "flareon", "espeon", "umbreon", "leafeon", "glaceon", "sylveon"], evolucoes_proximas("eevee"), self)
        assert_equals_unordered_list(["hitmonlee", "hitmonchan", "hitmontop"], evolucoes_proximas("tyrogue"), self)
        assert_equals_unordered_list(["poliwhirl"], evolucoes_proximas("poliwag"), self)
        assert_equals_unordered_list(["gloom"], evolucoes_proximas("oddish"), self)
        assert_equals_unordered_list(["poliwrath", "politoed"], evolucoes_proximas("poliwhirl"), self)
        assert_equals_unordered_list(["vileplume", "bellossom"], evolucoes_proximas("gloom"), self)

    @teste("Exercício 07", 1)
    def test_07d_ok_nao_tem_complexas(self):
        self.close()
        assert_equals_unordered_list([], evolucoes_proximas("espeon"), self)
        assert_equals_unordered_list([], evolucoes_proximas("leafeon"), self)
        assert_equals_unordered_list([], evolucoes_proximas("politoed"), self)
        assert_equals_unordered_list([], evolucoes_proximas("shedinja"), self)

    @teste("Exercício 07", 1)
    def test_07e_nao_existe(self):
        self.close()
        pokemon_nao_existe(lambda : evolucoes_proximas("dollynho"), self)
        pokemon_nao_existe(lambda : evolucoes_proximas("dobby"), self)
        pokemon_nao_existe(lambda : evolucoes_proximas("peppa-pig"), self)
        pokemon_nao_existe(lambda : evolucoes_proximas("batman"), self)
        pokemon_nao_existe(lambda : evolucoes_proximas("spiderman"), self)

    @teste("Exercício 07", 1)
    def test_07f_vazio(self):
        self.close()
        pokemon_nao_existe(lambda : evolucoes_proximas(""), self)

    @teste("Exercício 08", 5)
    def test_08a_simples(self):
        self.close()
        self.assertEqual(nivel_do_pokemon("blastoise",   110000), 49) # 4
        self.assertEqual(nivel_do_pokemon("mewtwo",     1000000), 92) # 1
        self.assertEqual(nivel_do_pokemon("magikarp",       900),  8) # 1
        self.assertEqual(nivel_do_pokemon("magikarp",   1000000), 92) # 1
        self.assertEqual(nivel_do_pokemon("slowbro",      65000), 40) # 2
        self.assertEqual(nivel_do_pokemon("octillery",   280000), 65) # 2
        self.assertEqual(nivel_do_pokemon("fraxure",     280000), 60) # 1
        self.assertEqual(nivel_do_pokemon("lunatone",     20000), 29) # 3
        self.assertEqual(nivel_do_pokemon("skitty",       50000), 39) # 3
        self.assertEqual(nivel_do_pokemon("torchic",      40000), 35) # 4
        self.assertEqual(nivel_do_pokemon("oddish",        5000), 19) # 4

    @teste("Exercício 08", 5)
    def test_08b_complexos(self):
        self.close()
        self.assertEqual(nivel_do_pokemon("zangoose",      9000), 17) # 5
        self.assertEqual(nivel_do_pokemon("milotic",      65000), 37) # 5
        self.assertEqual(nivel_do_pokemon("lumineon",    160000), 55) # 5
        self.assertEqual(nivel_do_pokemon("ninjask",     300000), 72) # 5
        self.assertEqual(nivel_do_pokemon("zangoose",    580000), 97) # 5
        self.assertEqual(nivel_do_pokemon("makuhita",       600), 10) # 6
        self.assertEqual(nivel_do_pokemon("gulpin",        7000), 21) # 6
        self.assertEqual(nivel_do_pokemon("seviper",     150000), 50) # 6
        self.assertEqual(nivel_do_pokemon("drifblim",   1000000), 87) # 6

    @teste("Exercício 08", 1)
    def test_08c_limites(self):
        self.close()
        self.assertEqual(nivel_do_pokemon("pinsir",           0),   1) # 1
        self.assertEqual(nivel_do_pokemon("bibarel",          0),   1) # 2
        self.assertEqual(nivel_do_pokemon("aipom",            0),   1) # 3
        self.assertEqual(nivel_do_pokemon("makuhita",         0),   1) # 6
        self.assertEqual(nivel_do_pokemon("magikarp",      1249),   9) # 1
        self.assertEqual(nivel_do_pokemon("metapod",        999),   9) # 2
        self.assertEqual(nivel_do_pokemon("magikarp",      1250),  10) # 1
        self.assertEqual(nivel_do_pokemon("butterfree",    1000),  10) # 2
        self.assertEqual(nivel_do_pokemon("charmeleon",   29948),  32) # 4
        self.assertEqual(nivel_do_pokemon("charmeleon",   29949),  33) # 4
        self.assertEqual(nivel_do_pokemon("hariyama",     71676),  40) # 6
        self.assertEqual(nivel_do_pokemon("hariyama",     71677),  41) # 6
        self.assertEqual(nivel_do_pokemon("togepi",      799999),  99) # 3
        self.assertEqual(nivel_do_pokemon("gengar",     1059859),  99) # 4
        self.assertEqual(nivel_do_pokemon("zangoose",    599999),  99) # 5
        self.assertEqual(nivel_do_pokemon("swalot",     1639999),  99) # 6
        self.assertEqual(nivel_do_pokemon("sylveon",    1000000), 100) # 2
        self.assertEqual(nivel_do_pokemon("jigglypuff", 1000000), 100) # 3
        self.assertEqual(nivel_do_pokemon("ledian",      800000), 100) # 3
        self.assertEqual(nivel_do_pokemon("vaporeon", 999999999), 100) # 2
        self.assertEqual(nivel_do_pokemon("vileplume",  1059860), 100) # 4
        self.assertEqual(nivel_do_pokemon("zangoose",    600000), 100) # 5
        self.assertEqual(nivel_do_pokemon("swalot",     1640000), 100) # 6

    @teste("Exercício 08", 1)
    def test_08d_nao_existe(self):
        self.close()
        pokemon_nao_existe(lambda : nivel_do_pokemon("dollynho", 1234), self)
        pokemon_nao_existe(lambda : nivel_do_pokemon("dobby", 1234), self)
        pokemon_nao_existe(lambda : nivel_do_pokemon("peppa-pig", 1234), self)
        pokemon_nao_existe(lambda : nivel_do_pokemon("batman", 1234), self)
        pokemon_nao_existe(lambda : nivel_do_pokemon("spiderman", 1234), self)

    @teste("Exercício 08", 1)
    def test_08e_vazio(self):
        self.close()
        pokemon_nao_existe(lambda : nivel_do_pokemon("", 1234), self)

    @teste("Exercício 08", 1)
    def test_08f_negativo(self):
        self.close()
        valor_errado(lambda : nivel_do_pokemon("pikachu",   -1), self)
        valor_errado(lambda : nivel_do_pokemon("pikachu",   -2), self)
        valor_errado(lambda : nivel_do_pokemon("pikachu", -666), self)

    @teste("Exercício 09", 5)
    def test_09a_simples(self):
        self.close()
        api_wobbuffet = EspeciePokemon.por_nome("wobbuffet")
        self.assertEqual(api_wobbuffet.nome, "wobbuffet")
        self.assertEqual(api_wobbuffet.cor, "azul")
        self.assertEqual(api_wobbuffet.evoluiu_de, 'wynaut')
        self.assertEqual(api_wobbuffet.evolui_para, [])

    @teste("Exercício 09", 3)
    def test_09b_complexo(self):
        self.close()
        api_gloom = EspeciePokemon.por_nome("gloom")
        self.assertEqual(api_gloom.nome, "gloom")
        self.assertEqual(api_gloom.cor, "azul")
        self.assertEqual(api_gloom.evoluiu_de, "oddish")

    @teste("Exercício 09", 1)
    def test_09c_complexo(self):
        self.close()
        api_gloom = EspeciePokemon.por_nome("gloom")
        self.assertEqual(api_gloom.evolui_para, ["vileplume", "bellossom"])

    @teste("Exercício 09", 1)
    def test_09d_nao_existe(self):
        self.close()
        pokemon_nao_existe(lambda : EspeciePokemon.por_nome("dollynho"), self)
        pokemon_nao_existe(lambda : EspeciePokemon.por_nome("dobby"), self)
        pokemon_nao_existe(lambda : EspeciePokemon.por_nome("peppa-pig"), self)
        pokemon_nao_existe(lambda : EspeciePokemon.por_nome("batman"), self)
        pokemon_nao_existe(lambda : EspeciePokemon.por_nome("spiderman"), self)

    @teste("Exercício 09", 1)
    def test_09e_vazio(self):
        self.close()
        pokemon_nao_existe(lambda : EspeciePokemon.por_nome(""), self)

    @teste("Exercício 10", 10)
    def test_10a_ok(self):
        self.reset()
        treinador_nao_cadastrado(lambda : detalhar_treinador("Ash Ketchum"), self)
        self.assertTrue(cadastrar_treinador("Ash Ketchum"))
        self.assertEqual(detalhar_treinador("Ash Ketchum"), {})

        treinador_nao_cadastrado(lambda : detalhar_treinador("Misty"), self)
        self.assertTrue(cadastrar_treinador("Misty"))
        self.assertEqual(detalhar_treinador("Misty"), {})

        resposta = requests.get(f"{site_treinador}/treinador", timeout = limite)
        self.assertEqual(resposta.json(), {
            "Ash Ketchum": {
                "nome": "Ash Ketchum", "pokemons": {}
            },
            "Misty": {
                "nome": "Misty", "pokemons": {}
            }
        })

    @teste("Exercício 10", 1)
    def test_10b_limpeza(self):
        self.reset()
        self.assertTrue(cadastrar_treinador("Jessie"))
        self.assertTrue(cadastrar_treinador("James"))
        self.reset()
        treinador_nao_cadastrado(lambda : detalhar_treinador("Jessie"), self)
        treinador_nao_cadastrado(lambda : detalhar_treinador("James"), self)

    @teste("Exercício 10", 2)
    def test_10c_repetido(self):
        self.reset()
        self.assertTrue(cadastrar_treinador("Jessie"))
        self.assertFalse(cadastrar_treinador("Jessie"))
        self.assertEqual(detalhar_treinador("Jessie"), {})
        Pokemon("Jessie", "A", arbok, 20000, Genero.MASCULINO).cadastrar()
        Pokemon("Jessie", "B", wobbuffet, 2000, Genero.MASCULINO).cadastrar()
        Pokemon("Jessie", "C", lickitung, 2500, Genero.MASCULINO).cadastrar()
        self.assertFalse(cadastrar_treinador("Jessie"))

        resposta = requests.get(f"{site_treinador}/treinador", timeout = limite)
        self.assertEqual(resposta.json(), {
            "Jessie": {
                "nome": "Jessie",
                "pokemons": {
                    "A": {"apelido": "A", "genero": "masculino", "tipo": "arbok", "experiencia": 20000},
                    "B": {"apelido": "B", "genero": "masculino", "tipo": "wobbuffet", "experiencia": 2000},
                    "C": {"apelido": "C", "genero": "masculino", "tipo": "lickitung", "experiencia": 2500}
                }
            }
        })

    @teste("Exercício 11", 10)
    def test_11a_ok(self):
        self.reset()
        pk = Pokemon("Homer Simpson", "Bart", pikachu, 50000, Genero.MASCULINO)
        self.assertEqual(pk.nivel, 36)

        mp = Pokemon("Homer Simpson", "Bart", magikarp, 1250, Genero.MASCULINO)
        self.assertEqual(mp.nivel, 10)

    @teste("Exercício 12", 8)
    def test_12a_ok(self):
        self.reset()
        self.assertTrue(cadastrar_treinador("Ash Ketchum"))
        Pokemon("Ash Ketchum", "P", pikachu, 50000, Genero.MASCULINO).cadastrar()
        self.assertTrue(cadastrar_treinador("Misty"))
        Pokemon("Misty", "A", staryu, 10000, Genero.MASCULINO).cadastrar()
        Pokemon("Misty", "B", staryu, 12000, Genero.FEMININO).cadastrar()
        self.assertTrue(cadastrar_treinador("Brock"))
        Pokemon("Brock", "O", onix, 8000, Genero.MASCULINO).cadastrar()
        Pokemon("Brock", "G", geodude, 20000, Genero.MASCULINO).cadastrar()
        self.assertTrue(cadastrar_treinador("James"))
        Pokemon("James", "A", koffing, 5000, Genero.MASCULINO).cadastrar()
        Pokemon("James", "B", victreebel, 20000, Genero.MASCULINO).cadastrar()

        resposta = requests.get(f"{site_treinador}/treinador", timeout = limite)
        self.assertEqual(resposta.json(), {
            "Ash Ketchum": {
                "nome": "Ash Ketchum",
                "pokemons": {
                    "P": {"apelido": "P", "tipo": "pikachu", "experiencia": 50000, "genero": "masculino"}
                }
            },
            "Misty": {
                "nome": "Misty",
                "pokemons": {
                    "A": {"apelido": "A", "tipo": "staryu", "experiencia": 10000, "genero": "masculino"},
                    "B": {"apelido": "B", "tipo": "staryu", "experiencia": 12000, "genero": "feminino"}
                }
            },
            "Brock": {
                "nome": "Brock",
                "pokemons": {
                    "O": {"apelido": "O", "tipo": "onix", "experiencia": 8000, "genero": "masculino"},
                    "G": {"apelido": "G", "tipo": "geodude", "experiencia": 20000, "genero": "masculino"}
                }
            },
            "James": {
                "nome": "James",
                "pokemons": {
                    "A": {"apelido": "A", "tipo": "koffing", "experiencia": 5000, "genero": "masculino"},
                    "B": {"apelido": "B", "tipo": "victreebel", "experiencia": 20000, "genero": "masculino"}
                }
            }
        })

    @teste("Exercício 12", 1)
    def test_12b_treinador_nao_existe(self):
        self.reset()
        treinador_nao_cadastrado(lambda : Pokemon("Max", "D", magikarp, 40000, Genero.FEMININO).cadastrar(), self)
        resposta = requests.get(f"{site_treinador}/treinador", timeout = limite)
        self.assertEqual(resposta.json(), {})

    @teste("Exercício 12", 1)
    def test_12c_pokemon_nao_existe(self):
        self.reset()
        self.assertTrue(cadastrar_treinador("Iris"))
        homer = EspeciePokemon("homer", "amarelo", "abe", ["bart", "lisa", "meggie"])
        pokemon_nao_existe(lambda : Pokemon("Iris", "D", homer, 40000, Genero.MASCULINO).cadastrar(), self)
        resposta = requests.get(f"{site_treinador}/treinador", timeout = limite)
        self.assertEqual(resposta.json(), {
            "Iris": {
                "nome": "Iris", "pokemons": {}
            }
        })

    @teste("Exercício 12", 2)
    def test_12d_pokemon_ja_existe(self):
        self.reset()
        self.assertTrue(cadastrar_treinador("Misty"))
        Pokemon("Misty", "estrela", staryu, 40000, Genero.FEMININO).cadastrar()
        pokemon_ja_cadastrado(lambda : Pokemon("Misty", "estrela", magikarp, 100, Genero.FEMININO).cadastrar(), self)

        resposta = requests.get(f"{site_treinador}/treinador", timeout = limite)
        self.assertEqual(resposta.json(), {
            "Misty": {
                "nome": "Misty", "pokemons": {
                    "estrela": {"apelido": "estrela", "tipo": "staryu", "experiencia": 40000, "genero": "feminino"}
                }
            }
        })

    @teste("Exercício 12", 1)
    def test_12e_treinador_errado(self):
        self.reset()
        self.assertTrue(cadastrar_treinador("Ash Ketchum"))
        treinador_nao_cadastrado(lambda : Pokemon("Gary", "pi", pikachu, 40000, Genero.MASCULINO).cadastrar(), self)
        resposta = requests.get(f"{site_treinador}/treinador", timeout = limite)
        self.assertEqual(resposta.json(), {
            "Ash Ketchum": {
                "nome": "Ash Ketchum", "pokemons": {}
            }
        })

    @teste("Exercício 13", 10)
    def test_13a_ok(self):
        self.reset()
        self.assertTrue(cadastrar_treinador("Ash Ketchum"))
        p1 = Pokemon("Ash Ketchum", "P", pikachu, 50000, Genero.MASCULINO)
        p1.cadastrar()
        p1.ganhar_experiencia(1500)
        self.assertEqual(p1.experiencia, 51500)

        self.assertTrue(cadastrar_treinador("James"))
        p2 = Pokemon("James", "P", weezing, 10000, Genero.MASCULINO)
        p2.cadastrar()
        Pokemon("James", "Q", victreebel, 12000, Genero.MASCULINO).cadastrar()
        p2.ganhar_experiencia(2500)
        self.assertEqual(p2.experiencia, 12500)

        resposta = requests.get(f"{site_treinador}/treinador", timeout = limite)
        self.assertEqual(resposta.json(), {
            "Ash Ketchum": {
                "nome": "Ash Ketchum", "pokemons": {
                    "P": {"apelido": "P", "tipo": "pikachu", "experiencia": 51500, "genero": "masculino"}
                }
            },
            "James": {
                "nome": "James", "pokemons": {
                    "P": {"apelido": "P", "tipo": "weezing", "experiencia": 12500, "genero": "masculino"},
                    "Q": {"apelido": "Q", "tipo": "victreebel", "experiencia": 12000, "genero": "masculino"}
                }
            }
        })

    @teste("Exercício 13", 1)
    def test_13b_treinador_nao_existe(self):
        self.reset()
        treinador_nao_cadastrado(lambda : Pokemon("Cilan", "bob-esponja", magikarp, 1000, Genero.FEMININO).ganhar_experiencia(10000), self)
        resposta = requests.get(f"{site_treinador}/treinador", timeout = limite)
        self.assertEqual(resposta.json(), {})

    @teste("Exercício 13", 1)
    def test_13c_pokemon_nao_existe(self):
        self.reset()
        self.assertTrue(cadastrar_treinador("Bonnie"))
        pokemon_nao_cadastrado(lambda : Pokemon("Bonnie", "bob-esponja", magikarp, 1000, Genero.FEMININO).ganhar_experiencia(10000), self)

        resposta = requests.get(f"{site_treinador}/treinador", timeout = limite)
        self.assertEqual(resposta.json(), {
            "Bonnie": {
                "nome": "Bonnie", "pokemons": {}
            }
        })

    @teste("Exercício 13", 1)
    def test_13d_erro_experiencia_negativa(self):
        self.reset()
        self.assertTrue(cadastrar_treinador("Dona Florinda"))
        quico = Pokemon("Dona Florinda", "Quico", arbok, 500, Genero.MASCULINO)
        quico.cadastrar()
        valor_errado(lambda : quico.ganhar_experiencia(  -1), self)
        valor_errado(lambda : quico.ganhar_experiencia(  -2), self)
        valor_errado(lambda : quico.ganhar_experiencia(-666), self)

    @teste("Exercício 14", 8)
    def test_14a_ok(self):
        self.reset()
        self.assertTrue(cadastrar_treinador("Ash Ketchum"))
        Pokemon("Ash Ketchum", "P", pikachu, 50000, Genero.MASCULINO).cadastrar()
        fazer_bonus = True

        self.assertTrue(cadastrar_treinador("James"))
        Pokemon("James", "P", weezing, 10000, Genero.MASCULINO).cadastrar()
        Pokemon("James", "Q", gloom, 12000, Genero.FEMININO).cadastrar()

        algum_pikachu = Pokemon.localizar_pokemon("Ash Ketchum", "P")
        algum_weezing = Pokemon.localizar_pokemon("James", "P")
        algum_gloom = Pokemon.localizar_pokemon("James", "Q")

        self.assertIs(type(algum_pikachu), Pokemon)
        self.assertEqual(algum_pikachu.nome_treinador, "Ash Ketchum")
        self.assertEqual(algum_pikachu.apelido, "P")
        self.assertEqual(algum_pikachu.genero, Genero.MASCULINO)
        self.assertEqual(algum_pikachu.tipo.nome, "pikachu")
        self.assertEqual(algum_pikachu.experiencia, 50000)
        self.assertEqual(algum_pikachu.nivel, 36)
        self.assertEqual(algum_pikachu.tipo.cor, "amarelo")
        self.assertEqual(algum_pikachu.tipo.evoluiu_de, "pichu")

        self.assertIs(type(algum_weezing), Pokemon)
        self.assertEqual(algum_weezing.nome_treinador, "James")
        self.assertEqual(algum_weezing.apelido, "P")
        self.assertEqual(algum_weezing.genero, Genero.MASCULINO)
        self.assertEqual(algum_weezing.tipo.nome, "weezing")
        self.assertEqual(algum_weezing.experiencia, 10000)
        self.assertEqual(algum_weezing.nivel, 21)
        self.assertEqual(algum_weezing.tipo.cor, "roxo")
        self.assertEqual(algum_weezing.tipo.evoluiu_de, "koffing")
        assert_equals_unordered_list([], algum_weezing.tipo.evolui_para, self)

        self.assertIs(type(algum_gloom), Pokemon)
        self.assertEqual(algum_gloom.nome_treinador, "James")
        self.assertEqual(algum_gloom.apelido, "Q")
        self.assertEqual(algum_gloom.genero, Genero.FEMININO)
        self.assertEqual(algum_gloom.tipo.nome, "gloom")
        self.assertEqual(algum_gloom.experiencia, 12000)
        self.assertEqual(algum_gloom.nivel, 25)
        self.assertEqual(algum_gloom.tipo.cor, "azul")
        self.assertEqual(algum_gloom.tipo.evoluiu_de, "oddish")
        
        global bonus_check
        def extra():
            assert_equals_unordered_list(["raichu"], algum_pikachu.tipo.evolui_para, self)
            assert_equals_unordered_list(["vileplume", "bellossom"], algum_gloom.tipo.evolui_para, self)
        bonus_check = extra

    @teste("Exercício 14", 1)
    def test_14b_bonus(self):
        bonus_check()

    @teste("Exercício 14", 1)
    def test_14c_treinador_nao_existe(self):
        self.reset()
        treinador_nao_cadastrado(lambda : Pokemon.localizar_pokemon("Cilan", "bob-esponja"), self)
        resposta = requests.get(f"{site_treinador}/treinador", timeout = limite)
        self.assertEqual(resposta.json(), {})

    @teste("Exercício 14", 1)
    def test_14d_pokemon_nao_existe(self):
        self.reset()
        self.assertTrue(cadastrar_treinador("Bonnie"))
        pokemon_nao_cadastrado(lambda : Pokemon.localizar_pokemon("Bonnie", "bob-esponja"), self)

        resposta = requests.get(f"{site_treinador}/treinador", timeout = limite)
        self.assertEqual(resposta.json(), {
            "Bonnie": {
                "nome": "Bonnie", "pokemons": {}
            }
        })

    @teste("Exercício 14", 2)
    def test_14e_treinador_errado(self):
        self.reset()
        self.assertTrue(cadastrar_treinador("Serena"))
        self.assertTrue(cadastrar_treinador("Dawn"))
        Pokemon("Serena", "fen", arbok, 5000, Genero.FEMININO).cadastrar()
        pokemon_nao_cadastrado(lambda : Pokemon.localizar_pokemon("Dawn", "fen"), self)

        resposta = requests.get(f"{site_treinador}/treinador", timeout = limite)
        self.assertEqual(resposta.json(), {
            "Serena": {
                "nome": "Serena", "pokemons": {
                    "fen": {"apelido": "fen", "tipo": "arbok", "experiencia": 5000, "genero": "feminino"}
                }
            },
            "Dawn": {
                "nome": "Dawn", "pokemons": {}
            }
        })

    @teste("Exercício 15", 10)
    def test_15a_ok(self):
        self.reset()
        self.assertTrue(cadastrar_treinador("Ash Ketchum"))
        Pokemon("Ash Ketchum", "P", pikachu, 50000, Genero.MASCULINO).cadastrar()

        self.assertTrue(cadastrar_treinador("James"))
        Pokemon("James", "P", weezing, 10000, Genero.MASCULINO).cadastrar()
        Pokemon("James", "Q", weepinbell, 12000, Genero.FEMININO).cadastrar()

        ash = detalhar_treinador("Ash Ketchum")
        james = detalhar_treinador("James")

        self.assertEqual(ash, {"P": "pikachu"})
        self.assertEqual(james, {"P": "weezing", "Q": "weepinbell"})

    @teste("Exercício 15", 1)
    def test_15b_treinador_nao_existe(self):
        self.reset()
        treinador_nao_cadastrado(lambda : detalhar_treinador("Cilan"), self)
        resposta = requests.get(f"{site_treinador}/treinador", timeout = limite)
        self.assertEqual(resposta.json(), {})

    @teste("Exercício 16", 10)
    def test_16a_ok(self):
        self.reset()
        self.assertTrue(cadastrar_treinador("Ash Ketchum"))
        Pokemon("Ash Ketchum", "P", pikachu, 50000, Genero.MASCULINO).cadastrar()

        self.assertTrue(cadastrar_treinador("Prof. Carvalho"))

        self.assertTrue(cadastrar_treinador("James"))
        Pokemon("James", "P", weezing, 10000, Genero.MASCULINO).cadastrar()
        Pokemon("James", "Q", weepinbell, 12000, Genero.FEMININO).cadastrar()

        excluir_treinador("Ash Ketchum")

        resposta1 = requests.get(f"{site_treinador}/treinador", timeout = limite)
        self.assertEqual(resposta1.json(), {
            "James": {
                "nome": "James", "pokemons": {
                    "P": {"apelido": "P", "tipo": "weezing", "experiencia": 10000, "genero": "masculino"},
                    "Q": {"apelido": "Q", "tipo": "weepinbell", "experiencia": 12000, "genero": "feminino"}
                }
            },
            "Prof. Carvalho": {
                "nome": "Prof. Carvalho", "pokemons": {}
            }
        })
        treinador_nao_cadastrado(lambda : detalhar_treinador("Ash Ketchum"), self)
        treinador_nao_cadastrado(lambda : Pokemon.localizar_pokemon("Ash Ketchum", "P"), self)

        excluir_treinador("James")

        resposta2 = requests.get(f"{site_treinador}/treinador", timeout = limite)
        self.assertEqual(resposta2.json(), {
            "Prof. Carvalho": {"nome": "Prof. Carvalho", "pokemons": {}}
        })
        treinador_nao_cadastrado(lambda : detalhar_treinador("James"), self)
        treinador_nao_cadastrado(lambda : Pokemon.localizar_pokemon("James", "P"), self)
        treinador_nao_cadastrado(lambda : Pokemon.localizar_pokemon("James", "Q"), self)

        excluir_treinador("Prof. Carvalho")

        resposta3 = requests.get(f"{site_treinador}/treinador", timeout = limite)
        self.assertEqual(resposta3.json(), {})
        treinador_nao_cadastrado(lambda : detalhar_treinador("Prof. Carvalho"), self)

    @teste("Exercício 16", 1)
    def test_16b_treinador_nao_existe(self):
        self.reset()
        treinador_nao_cadastrado(lambda : excluir_treinador("Kiawe"), self)
        resposta1 = requests.get(f"{site_treinador}/treinador", timeout = limite)
        self.assertEqual(resposta1.json(), {})

        self.assertTrue(cadastrar_treinador("Kiawe"))
        Pokemon("Kiawe", "c", charizard, 50000, Genero.MASCULINO).cadastrar()
        treinador_nao_cadastrado(lambda : excluir_treinador("Lillie"), self)
        resposta2 = requests.get(f"{site_treinador}/treinador", timeout = limite)
        self.assertEqual(resposta2.json(), {
            "Kiawe": {
                "nome": "Kiawe", "pokemons": {
                    "c": {"apelido": "c", "tipo": "charizard", "experiencia": 50000, "genero": "masculino"}
                }
            }
        })

        excluir_treinador("Kiawe")
        resposta3 = requests.get(f"{site_treinador}/treinador", timeout = limite)
        self.assertEqual(resposta3.json(), {})

    @teste("Exercício 17", 10)
    def test_17a_ok(self):
        self.reset()
        self.assertTrue(cadastrar_treinador("Ash Ketchum"))
        Pokemon("Ash Ketchum", "P", pikachu, 50000, Genero.MASCULINO).cadastrar()

        self.assertTrue(cadastrar_treinador("Prof. Carvalho"))

        self.assertTrue(cadastrar_treinador("James"))
        Pokemon("James", "P", weezing, 10000, Genero.MASCULINO).cadastrar()
        Pokemon("James", "Q", weepinbell, 12000, Genero.FEMININO).cadastrar()

        excluir_pokemon("Ash Ketchum", "P")

        resposta1 = requests.get(f"{site_treinador}/treinador", timeout = limite)
        self.assertEqual(resposta1.json(), {
            "Ash Ketchum": {
                "nome": "Ash Ketchum", "pokemons": {}
            },
            "James": {
                "nome": "James", "pokemons": {
                    "P": {"apelido": "P", "tipo": "weezing", "experiencia": 10000, "genero": "masculino"},
                    "Q": {"apelido": "Q", "tipo": "weepinbell", "experiencia": 12000, "genero": "feminino"}
                }
            },
            "Prof. Carvalho": {
                "nome": "Prof. Carvalho", "pokemons": {}
            }
        })
        pokemon_nao_cadastrado(lambda : Pokemon.localizar_pokemon("Ash Ketchum", "P"), self)
        Pokemon.localizar_pokemon("James", "P")
        Pokemon.localizar_pokemon("James", "Q")

        excluir_pokemon("James", "Q")

        resposta2 = requests.get(f"{site_treinador}/treinador", timeout = limite)
        self.assertEqual(resposta2.json(), {
            "Ash Ketchum": {
                "nome": "Ash Ketchum", "pokemons": {}
            },
            "James": {
                "nome": "James", "pokemons": {
                    "P": {"apelido": "P", "tipo": "weezing", "experiencia": 10000, "genero": "masculino"}
                }
            },
            "Prof. Carvalho": {
                "nome": "Prof. Carvalho", "pokemons": {}
            }
        })
        pokemon_nao_cadastrado(lambda : Pokemon.localizar_pokemon("Ash Ketchum", "P"), self)
        Pokemon.localizar_pokemon("James", "P")
        pokemon_nao_cadastrado(lambda : Pokemon.localizar_pokemon("James", "Q"), self)

        excluir_pokemon("James", "P")

        resposta3 = requests.get(f"{site_treinador}/treinador", timeout = limite)
        self.assertEqual(resposta3.json(), {
            "Ash Ketchum": {
                "nome": "Ash Ketchum", "pokemons": {}
            },
            "James": {
                "nome": "James", "pokemons": {}
            },
            "Prof. Carvalho": {
                "nome": "Prof. Carvalho", "pokemons": {}
            }
        })
        pokemon_nao_cadastrado(lambda : Pokemon.localizar_pokemon("Ash Ketchum", "P"), self)
        pokemon_nao_cadastrado(lambda : Pokemon.localizar_pokemon("James", "P"), self)
        pokemon_nao_cadastrado(lambda : Pokemon.localizar_pokemon("James", "Q"), self)

    @teste("Exercício 17", 1)
    def test_17b_treinador_nao_existe(self):
        self.reset()
        self.assertTrue(cadastrar_treinador("Kiawe"))
        Pokemon("Kiawe", "c", charizard, 50000, Genero.MASCULINO).cadastrar()
        treinador_nao_cadastrado(lambda : excluir_pokemon("Lillie", "c"), self)
        resposta1 = requests.get(f"{site_treinador}/treinador", timeout = limite)
        self.assertEqual(resposta1.json(), {
            "Kiawe": {
                "nome": "Kiawe", "pokemons": {
                    "c": {"apelido": "c", "tipo": "charizard", "experiencia": 50000, "genero": "masculino"}
                }
            }
        })

        Pokemon.localizar_pokemon("Kiawe", "c")
        resposta2 = requests.get(f"{site_treinador}/treinador", timeout = limite).json()
        self.assertEqual(resposta2, {
            "Kiawe": {
                "nome": "Kiawe", "pokemons": {
                    "c": {"apelido": "c", "tipo": "charizard", "experiencia": 50000, "genero": "masculino"}
                }
            }
        })

    @teste("Exercício 17", 1)
    def test_17c_pokemon_nao_existe(self):
        self.reset()
        self.assertTrue(cadastrar_treinador("Kiawe"))
        Pokemon("Kiawe", "c", charizard, 50000, Genero.MASCULINO).cadastrar()
        pokemon_nao_cadastrado(lambda : excluir_pokemon("Kiawe", "d"), self)
        resposta1 = requests.get(f"{site_treinador}/treinador", timeout = limite)
        self.assertEqual(resposta1.json(), {
            "Kiawe": {
                "nome": "Kiawe", "pokemons": {
                    "c": {"apelido": "c", "tipo": "charizard", "experiencia": 50000, "genero": "masculino"}
                }
            }
        })

        Pokemon.localizar_pokemon("Kiawe", "c")
        resposta2 = requests.get(f"{site_treinador}/treinador", timeout = limite)
        self.assertEqual(resposta2.json(), {
            "Kiawe": {
                "nome": "Kiawe", "pokemons": {
                    "c": {"apelido": "c", "tipo": "charizard", "experiencia": 50000, "genero": "masculino"}
                }
            }
        })

        excluir_pokemon("Kiawe", "c")
        resposta3 = requests.get(f"{site_treinador}/treinador", timeout = limite)
        self.assertEqual(resposta3.json(), {
            "Kiawe": {
                "nome": "Kiawe", "pokemons": {}
            }
        })

    @teste("Exercício 17", 1)
    def test_17d_limpeza(self):
        self.reset()
        self.assertTrue(cadastrar_treinador("Tracey"))
        alguma_magikarp = Pokemon("Tracey", "m", magikarp, 40000, Genero.MASCULINO)
        alguma_magikarp.cadastrar()

        self.reset()
        treinador_nao_cadastrado(lambda : detalhar_treinador("Tracey"), self)
        treinador_nao_cadastrado(lambda : Pokemon.localizar_pokemon("Tracey", "m"), self)
        treinador_nao_cadastrado(lambda : alguma_magikarp.ganhar_experiencia(4000), self)
        treinador_nao_cadastrado(lambda : Pokemon("Tracey", "t", staryu, 500, Genero.MASCULINO).cadastrar(), self)
        treinador_nao_cadastrado(lambda : alguma_magikarp.cadastrar(), self)
        treinador_nao_cadastrado(lambda : excluir_pokemon("Tracey", "t"), self)
        treinador_nao_cadastrado(lambda : excluir_treinador("Tracey"), self)

        resposta = requests.get(f"{site_treinador}/treinador", timeout = limite)
        self.assertEqual(resposta.json(), {})

    @teste("Não usar print", 0, penalidade = 20)
    def test_99a_print(self):
        sem_io.test_print()

    @teste("Não usar input", 0, penalidade = 40)
    def test_99b_input(self):
        sem_io.test_input()

def runTests():
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestPokemon)
    unittest.TextTestRunner(verbosity = 2, failfast = parar_no_primeiro_erro).run(suite)
    pontos_main.mostrar_pontos()

if __name__ == '__main__':
    try:
        resposta = requests.get(f"{site_pokeapi}/", timeout = limite)
        if resposta.status_code != 200: raise Exception()
    except:
        raise Exception("Não conseguiu conectar na PokéAPI. Abortando os testes.")

    try:
        resposta = requests.get(f"{site_treinador}/hello", timeout = limite)
        if resposta.status_code != 200 or resposta.text != "Pikachu, eu escolho você!": raise Exception()
    except:
        raise Exception("Não conseguiu conectar na API do treinador. Abortando os testes.")

    runTests()