import json
import itertools
from itertools import combinations

class Aluno:
    def __init__(self, nome, dias):
        self.nome = nome
        self.dias = dias
class AlunoNaoIT(Aluno):
    def __init__(self, nome, dias):
        super().__init__(nome, dias)
        self.Turmas2H = {}
        self.Turmas3H = {}
        self.Comb = {}

# Função para criar um grafo a partir da lista de alunos

def transform_value(value):
    if value == "":
        return "1"
    elif value == "X":
        return "0"

def transform_list(lst):
    return [transform_value(item) for item in lst]

def find_student_by_name(name, alunos):
    for i, aluno in enumerate(alunos):
        if aluno.nome == name:
            return alunos.pop(i)
    return None

def generate_combinations(dias, interval_hours):
    combinations = []
    current_combination = []

    for i, value in enumerate(dias):
        if value == '1':
            current_combination.append(i)
            if len(current_combination) == interval_hours:
                combinations.append(tuple(current_combination))
                current_combination.pop(0)
        else:
            current_combination = []

    return combinations

with open(r'C:\Users\range\Downloads\dados.json', "r") as json_file:
    data = json.load(json_file)

diasSemana=["Segunda","Terca","Quarta","Quinta","Sexta"]
alunos = []
it_aluno = Aluno("nome", [])

for aluno_json in data:
    nome = aluno_json["Nome"]
    dias_json = aluno_json["Dias"]
    dias = {
        "Segunda": transform_list(dias_json["Segunda"]),
        "Terca": transform_list(dias_json["Terca"]),
        "Quarta": transform_list(dias_json["Quarta"]),
        "Quinta": transform_list(dias_json["Quinta"]),
        "Sexta": transform_list(dias_json["Sexta"])
    }
    if(nome != "IT"):
        aluno = AlunoNaoIT(nome, dias)
        alunos.append(aluno)
    else:
        it_aluno = Aluno(nome, dias)

alunoT = find_student_by_name("T", alunos)

alunos.pop(0)

Turmas2HGlobal = {}
Turmas3HGlobal = {}

if it_aluno:
    for dia, horarios in it_aluno.dias.items():
        combinations_2h = generate_combinations(horarios, interval_hours=2)
        combinations_3h = generate_combinations(horarios, interval_hours=3)

        Turmas2HGlobal[dia] = combinations_2h
        Turmas3HGlobal[dia] = combinations_3h

   # print("Turmas2HGlobal:")
    #print(Turmas2HGlobal)
   # print("Turmas3HGlobal:")
    #print(Turmas3HGlobal)
else:
    print("Aluno IT não encontrado.")

for aluno in alunos:
    for dia, horarios in aluno.dias.items():
        combinations_2h = generate_combinations(horarios, interval_hours=2)
        combinations_3h = generate_combinations(horarios, interval_hours=3)
        aluno.Turmas2H[dia] = combinations_2h
        aluno.Turmas3H[dia] = combinations_3h
    #print(aluno.nome)
    #print("Turmas 2H:")
    #print(aluno.Turmas2H)
    #print("Turmas 3H:")
    #print(aluno.Turmas3H)

alunoT = find_student_by_name("S", alunos)
if alunoT:
    print("CombinaçõesT de 2 horas para Segunda-feira:")
    print(alunoT.Turmas2H['Segunda'])

    print("CombinaçõesT de 3 horas para Segunda-feira:")
    print(alunoT.Turmas3H["Segunda"])
else:
    print("Aluno R não encontrado.")

alunoX = find_student_by_name("A", alunos)

if alunoX:
    print("CombinaçõesX de 2 horas para Segunda-feira:")
    print(alunoX.Turmas2H['Segunda'])

    print("CombinaçõesX de 3 horas para Segunda-feira:")
    print(alunoX.Turmas3H["Segunda"])
else:
    print("Aluno R não encontrado.")

if alunoT and alunoX:
    dia_semana = "Segunda"  # vai mudando os dias

    if dia_semana in alunoT.Turmas2H and dia_semana in alunoX.Turmas2H:
        combinacoes_alunoT = set(alunoT.Turmas3H[dia_semana])
        combinacoes_alunoX = set(alunoX.Turmas3H[dia_semana])

        if combinacoes_alunoT.intersection(combinacoes_alunoX):
            print("Os alunos têm combinações em comum na Segunda-feira.")
            print(combinacoes_alunoT.intersection(combinacoes_alunoX))
        else:
            print("Os alunos não têm combinações em comum na Segunda-feira.")
            print(combinacoes_alunoT.intersection(combinacoes_alunoX))
    else:
        print("Dia da semana não encontrado para um dos alunos.")
else:
    print("Aluno T ou aluno X não encontrado.")
# to fazendo uma comparação de 1 pra todos
for alunoT in alunos:
    #dia_semana = "Segunda"  # Substitua pelo dia desejado
    combinacoes_alunoT = set(alunoT.Turmas3H[dia_semana])
    for dia_semana in diasSemana:
        for alunoX in alunos:
            if alunoX != alunoT and dia_semana in alunoX.Turmas2H:
                combinacoes_alunoX = set(alunoX.Turmas3H[dia_semana])

                if combinacoes_alunoT.intersection(combinacoes_alunoX):
                    print(f"O aluno {alunoT.nome} tem combinações em comum com o aluno {alunoX.nome} na {dia_semana}.")
                    print(combinacoes_alunoT.intersection(combinacoes_alunoX))
                    alunoT.Comb[alunoX.nome] = (combinacoes_alunoT.intersection(combinacoes_alunoX))
                else:
                    print(f"O aluno {alunoT.nome} não tem combinações em comum com o aluno {alunoX.nome} na {dia_semana}.")

