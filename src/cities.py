import requests
import random

class City:

    def __init__(self, name):
        self.name = name
        self.x = None
        self.y = None

    def set_coordinates(self):
        self.x = random.randint(0, 1000)
        self.y = random.randint(0, 1000)


class Cities:

    def __init__(self, uf):
        self.uf = uf
        self.uf_id = None
        self.list = []

        self.get_uf_id()
        self.get_list()

    def get_uf_id(self):
        URL = "https://servicodados.ibge.gov.br/api/v1/localidades/estados"

        r = requests.get(url = URL)
        data = r.json()

        for element in data:
            if element["nome"] == self.uf:
                self.uf_id = element["id"]

        if self.uf_id is None:
            print("ERRO: UF INVÁLIDA!")
            exit(1)

    def get_list(self):
        URL = "https://servicodados.ibge.gov.br/api/v1/localidades/estados/{}/municipios"

        print("Iniciando recuperação dos dados...")

        r = requests.get(url = URL.format(self.uf_id))
        data = r.json()

        for element in data:
            city = City(element["nome"])
            city.set_coordinates()

            while not self.verify_coordinates(city.x, city.y):
                city.set_coordinates()

            self.list.append(city)

        print("Dados recuperados com sucesso!")

    def verify_coordinates(self, x, y):
        for element in self.list:
            if element.x == x and element.y == y:
                return False
        return True

