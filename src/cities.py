import requests
import random
import csv

class City:

    def __init__(self, uf, uf_id, name):
        self.uf = uf
        self.uf_id = uf_id
        self.name = name
        self.population = -1
        self.x = None
        self.y = None

        self.set_population()

    def set_population(self):
        sheet_name = "../data/populacao.csv"
        
        with open(sheet_name, mode='r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0

            for row in csv_reader:
                if line_count > 1:
                    if row[0] == self.uf and row[2] == self.name:
                        self.population = int(row[3])
                        break
                line_count += 1

    def set_coordinates(self):
        sheet_name = "../data/coordenadas.csv"

        with open(sheet_name, mode='r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0

            for row in csv_reader:
                if line_count > 0:
                    if row[1] == self.name and row[5] == str(self.uf_id):
                        self.x = float(row[2])
                        self.y = float(row[3])
                        break
                line_count += 1


class Cities:

    def __init__(self, uf_name, population):
        self.uf_name = uf_name
        self.population = int(population)
        self.uf = ""
        self.uf_id = None
        self.list = []

        self.get_uf()
        self.get_list()

    def get_uf(self):
        URL = "https://servicodados.ibge.gov.br/api/v1/localidades/estados"

        r = requests.get(url = URL)
        data = r.json()

        for element in data:
            if element["nome"] == self.uf_name:
                self.uf = element["sigla"]
                self.uf_id = element["id"]

        if self.uf == "" or self.uf_id is None:
            print("\nERRO: UF INVÁLIDA!")
            exit(1)

    def get_list(self):
        URL = "https://servicodados.ibge.gov.br/api/v1/localidades/estados/{}/municipios"

        print("Iniciando recuperação dos dados...")

        r = requests.get(url = URL.format(self.uf_id))
        data = r.json()

        for element in data:
            city = City(self.uf, self.uf_id, element["nome"])

            if city.population > 0 and city.population <= self.population:
                city.set_coordinates()

                if city.x is not None and city.y is not None:
                    self.list.append(city)

        print("\nDados recuperados com sucesso!")

