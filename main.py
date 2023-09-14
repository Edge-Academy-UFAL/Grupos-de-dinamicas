import json
import copy
import random


class grup:
    def __int__(self, horario, integrantes):
        self.horario = horario
        self.integrantes = []

class Aluno:
    def __init__(self, nome, dias):
        self.nome = nome
        self.dias = dias


class AlunoNaoIT(Aluno):
    def __init__(self, nome, dias):
        super().__init__(nome, dias)
        self.Turmas2H = {}
        self.Turmas3H = {}
        self.Comb = {
            "Segunda": {},"Terca": {}, "Quarta": {}, "Quinta": {}, "Sexta": {},
            }
        self.temGP = 0

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
            current_combination.append(str(i))
            if len(current_combination) == interval_hours:
                combinations.append(''.join(current_combination))
                current_combination.pop(0)
        else:
            current_combination = []

    return combinations

""""" unused
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
"""""

with open(r'C:\Users\range\Downloads\dados.json', "r") as json_file:
    data = json.load(json_file)

diasSemana=["Segunda", "Terca", "Quarta", "Quinta", "Sexta"]
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
    if nome != "IT":
        aluno = AlunoNaoIT(nome, dias)
        alunos.append(aluno)
    else:
        it_aluno = Aluno(nome, dias)

#alunoT = find_student_by_name("T", alunos)

alunos.pop(0)

Turmas2HGlobal = {}
Turmas3HGlobal = {}

if it_aluno:
    for dia, horarios in it_aluno.dias.items():
        combinations_2h = generate_combinations(horarios, interval_hours=2)
        combinations_3h = generate_combinations(horarios, interval_hours=3)

        Turmas2HGlobal[dia] = combinations_2h
        Turmas3HGlobal[dia] = combinations_3h

    print("Turmas2HGlobal:")
    print(Turmas2HGlobal)
    print("Turmas3HGlobal:")
    print(Turmas3HGlobal)
else:
    print("Aluno IT não encontrado.")

for aluno in alunos:
    for dia, horarios in aluno.dias.items():
        combinations_2h = generate_combinations(horarios, interval_hours=2)
        combinations_3h = generate_combinations(horarios, interval_hours=3)
        aluno.Turmas2H[dia] = combinations_2h
        aluno.Turmas3H[dia] = combinations_3h
    print(aluno.nome)
    print("Turmas 2H:")
    print(aluno.Turmas2H)
    print("Turmas 3H:")
    print(aluno.Turmas3H)

"""""
for alunoT in alunos:
    #dia_semana = "Segunda"  # Substitua pelo dia desejado
    for dia_semana in diasSemana:
        combinacoes_alunoT = set(alunoT.Turmas3H[dia_semana])
        for alunoX in alunos:
            if alunoX != alunoT and dia_semana in alunoX.Turmas2H:
                combinacoes_alunoX = set(alunoX.Turmas3H[dia_semana])

                if combinacoes_alunoT.intersection(combinacoes_alunoX):
                    print(f"O aluno {alunoT.nome} tem combinações em comum com o aluno {alunoX.nome} na {dia_semana}.")
                    #print(combinacoes_alunoT.intersection(combinacoes_alunoX))
                    alunoT.Comb[dia_semana][alunoX.nome] = (combinacoes_alunoT.intersection(combinacoes_alunoX))
                    print(f'{alunoT.nome} e {alunoX.nome} : {alunoT.Comb[dia_semana][alunoX.nome]}')
                else:
                    print(f"O aluno {alunoT.nome} não tem combinações em comum com o aluno {alunoX.nome} na {dia_semana}.")

"""
quant = 20
gp_s = []
while len(gp_s) < 2:
    copyAlunos = list(copy.copy(alunos))
    random.shuffle(copyAlunos)
    #for a in copyAlunos:
        #a.temGP = 0
    for alunoT in copyAlunos:
        tan = 0
        #print(alunoT.nome)
        for dia_semana in diasSemana:

                    # print(f'conbinação atual {combinacoes_alunoT} ---- {gp}-----{dia_semana} ---- tan{tan}')

                    #if tan == 7:
                        #continue

            gp= ''
            #gp = alunoT.nome
            tan = 0
            combinacoes_alunoT = set(alunoT.Turmas3H[dia_semana])
            combinacoes_alunoTG = set(alunoT.Turmas3H[dia_semana])
            for alunoX in copyAlunos:
                if tan >= 7 or alunoX.temGP == 1:
                    continue
                if alunoX != alunoT and dia_semana in alunoX.Turmas2H:
                    combinacoes_alunoX = set(alunoX.Turmas3H[dia_semana])

                    if combinacoes_alunoT.intersection(combinacoes_alunoX) and combinacoes_alunoTG.intersection(combinacoes_alunoX) and tan < 8:
                        print(f"O aluno {alunoT.nome} tem combinações em comum com o aluno {alunoX.nome} na {dia_semana}.")
                        print(combinacoes_alunoTG.intersection(combinacoes_alunoX))
                        tan = tan + 1
                        alunoX.temGP = 1
                        #alunoT.temGP = 1
                        quant -= 1
                        #print(f' removi {alunoX.nome}')
                        #copyAlunos.remove(alunoT)
                        combinacoes_alunoTG = combinacoes_alunoTG.intersection(combinacoes_alunoX)
                        gp = gp + alunoX.nome
            if tan >= 6:
                flag = 1
                for g in gp_s:
                    if g == (gp + ' ' + dia_semana):
                        flag = 0
                # gp += alunoT.nome
                if flag == 1:
                    alunoT.temGP = 1

                    print(alunoT.nome)

                    gp_s.append(gp + ' ' + dia_semana)

                    print(gp)
                    print(len(gp_s))
                        #find_student_by_name(alunoX.nome, copyAlunos)
                        #copyAlunos.remove(alunoX)
                        #print(f'{alunoT.nome} e {alunoX.nome} : {alunoT.Comb[dia_semana][alunoX.nome]}')

                    #else:
                        #print(f"O aluno {alunoT.nome} não tem combinações em comum com o aluno {alunoX.nome} na {dia_semana}.")
    print(gp_s)
    print(f'restam {quant}')
def normalize_string(s):
    # Normaliza a string ordenando os caracteres em ordem alfabética
    return ''.join(sorted(s))

valores_unicos = set()

for s in gp_s:
    s_normalizada = normalize_string(s)
    valores_unicos.add(s_normalizada)

valores_unicos_lista = list(valores_unicos)

print(valores_unicos_lista)
"""
for alunoi in copyAlunos:
    for dia in diasSemana:
        for alunoj in copyAlunos:
            if alunoj== alunoi:
                continue
            diaSemanaj = set(alunoi.Comb[dia][alunoj.nome])
            diaSemanaj = list(diaSemanaj)
            for hora in diaSemanaj:
                for
"""
"""""
alunoX = copyAlunos.pop(0)
quarta = set(alunoX.Comb['Quarta']['M'])
quarta = list(quarta)
print(quarta[1])
#O aluno A tem combinações em comum com o aluno M na Quarta.
#A e M : {'123', '012'}
"""