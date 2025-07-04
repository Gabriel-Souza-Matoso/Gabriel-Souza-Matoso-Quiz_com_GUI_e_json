'''
=-=-=-=-=-Observações-=-=-=-=-=
As dificuldades média, difícil e extrema têm aproximmadamente 30% de chance de exibir uma pergunta de dificuldade inferior a ela.
A função pontuação, além de ser responsável por atualizar a pontuacao, tambem é responsável por atualizar os textos da GUI.
Eu preferi usar dicionarios em vez de vetores porque fica mais legivel e organizado.
Vão ser 10 perguntas para cada quiz.
O leaderboard ainda não está pronto, provavelmente eu termino amanhã.

----Pontuação-por-Acerto----
Fácil = +10
Média = +15
Difícil = +20
Extrema = +25
(caso não concorde, mude os valores nas linhas, 436~444)

----COMO-ADICIONAR-PERGUNTAS----
É de extrema importância seguir EXTAMENTE os passos a seguir

1 ir no modulo "perguntas_json"
2 abrir{
2 colocar "pergunta" : "a pergunta em questão aqui", <- é para colocar essa virgula
3 colocar "certa" : "a alternativa certa da qestão", <- é para colocar essa virgula
4 colocar "erradas" : [alternativa errada 1,  alternativa errada 2, alternativa errada 3 ] <- aqui NÂO tem virgula
5 fechar o dicionario usando }

se as intruções forem seguidas corretamente vai ficar assim:
    {
        "pergunta": "Qual é a capital do Brasil?",
        "certa": "Brasília",
        "erradas": ["Rio de Janeiro", "São Paulo", "Belo Horizonte"]
    }, <- colocar virgula SOMENTE se NÃO for o ultimo indice

----COMO-MUDAR-A-PALHETA-DE-CORES-DO-QUIZ----

para mudar a palheta de cores do quiz, você deve modificar os elementos do vetor "cores",
ele esta localizado em torno da linha 311 (apos os dicionarios de perguntas)
para modificar as pores voc~e deve modificar o codigo hexadecimal dentro do vetor, para colocar a cor que quiser

cores[0] -> fundo do quiz
cores[1] -> cor da fonte
cores[2] -> cor dos botões
'''
import tkinter.font
import json
from tkinter import *
import random

# =-=-=-=-=-=-=-VARIAVEIS-GLOBAIS-=-=-=-=-=-=-=
# --- perguntas salvas no json ---
with open("perguntas.json", "r", encoding= "utf-8") as textos_json:
    perguntas = json.load(textos_json)

# ---variaveis-dos-botoes---
perguntas_F = perguntas["perguntas_F"]
perguntas_M = perguntas["perguntas_M"]
perguntas_D = perguntas["perguntas_D"]
perguntas_E = perguntas["perguntas_E"]

cores = ["#2E3A59", "#F5F7FA", "#627D98", "#9FB3C8", "#1B4965"]
botao = [0,1,2,3]
letras_alternativas = ["A ", "B ", "C ", "D "]

# ---variaveis-que-guardam-dados---
guardar_perguntas_usadas = []
pergunta_atual = 0
quant_perguntas = 0
puxar_alternativas = []
pontos = 0
fonte_titulo, fonte_bot, fonte_ponto = 0, 0, 0
ler_vetor_atual = []
ler_erradas_atuais = []
dificuldade = 0

def gerar_perguntas():
    global pergunta_atual, guardar_perguntas_usadas, puxar_alternativas
    pergunta_atual = sortear_pergunta()
    guardar_perguntas_usadas.append(pergunta_atual)
    puxar_alternativas = list(sortear_alternativas())
    puxar_alternativas = texto_alternativas()


def dificuldades(a):
    match a:
        case 0:
            return "facil"
        case 1:
            return "medio"
        case 2:
            return "dificil"
        case 3:
            return "insana"

def apaque_bots():
    global botao, ponto_escrito
    ponto_escrito.destroy()
    for i in range(len(botao)):
       botao[i].destroy()
    del(botao)

def fontes():
    global fonte_bot, fonte_ponto, fonte_titulo, quant_perguntas
    fonte_titulo = tkinter.font.Font(family="Comic Sans MS", size=22, weight="bold")
    fonte_bot = tkinter.font.Font(family="arial", size=13, weight="bold")
    fonte_ponto = tkinter.font.Font(family="arial", size=10)

def sortear_pergunta():
    sortea_indice = random.randint(0, 10)
    if (sortea_indice not in guardar_perguntas_usadas):
        return sortea_indice
    else:
        while True:
            sortea_indice = random.randint(0, 10)
            if sortea_indice not in guardar_perguntas_usadas:
                return sortea_indice

def sortear_alternativas():
    num = []
    guarda_num = 0
    cont = 0
    while cont < 4:
        guarda_num = random.randint(1, 4)
        if guarda_num not in list(num):
            num.append(guarda_num)
            cont += 1
    del guarda_num
    del cont
    return list(num)

def texto_alternativas():
    global quant_perguntas, pergunta_atual, ler_vetor_atual, ler_erradas_atuais, puxar_alternativas
    if quant_perguntas == 0:
        puxar_alternativas = ["facil", "medio", "dificil", "insana"]
        quant_perguntas += 1
    else:
        a = 0
        quant_perguntas += 1
        match dificuldade:
            case "facil":
                ler_vetor_atual = perguntas_F[pergunta_atual]
            case "medio":
                a = random.randint(0,10)
                if(a < 3):
                    ler_vetor_atual = perguntas_F[pergunta_atual]
                else:
                    ler_vetor_atual = perguntas_M[pergunta_atual]

            case "dificil":
                a = random.randint(0, 10)
                if (a < 3):
                    ler_vetor_atual = perguntas_M[pergunta_atual]
                else:
                    ler_vetor_atual = perguntas_D[pergunta_atual]
            case "insana":
                a = random.randint(0, 10)
                if (a < 3):
                    ler_vetor_atual = perguntas_D[pergunta_atual]
                else:
                    ler_vetor_atual = perguntas_E[pergunta_atual]

        ler_erradas_atuais = ler_vetor_atual["erradas"]

        for i in range(0, len(puxar_alternativas), 1):
            match puxar_alternativas[i]:
                case 1:
                    puxar_alternativas[i] = ler_vetor_atual["certa"]
                case 2:
                    puxar_alternativas[i] = ler_erradas_atuais[0]
                case 3:
                    puxar_alternativas[i] = ler_erradas_atuais[1]
                case 4:
                    puxar_alternativas[i] = ler_erradas_atuais[2]
    return list(puxar_alternativas)

def pontuacao(a):
    global pontos, pergunta_atual, puxar_alternativas, ler_vetor_atual, dificuldade
    print(a)
    if quant_perguntas == 1:
        dificuldade = dificuldades(a)
        print(dificuldade)
        gerar_perguntas()
        titulo.config(text=str(ler_vetor_atual["pergunta"]))
        for i in range(0,3,1):
            botao[i].config(text= letras_alternativas[i] + str(puxar_alternativas[i]))
        ponto_escrito.config(text="PONTOS : " + str(pontos))
        return

    if puxar_alternativas[a] == ler_vetor_atual["certa"]:
        match dificuldade:
            case "facil":
                pontos += 10
            case "medio":
                pontos += 15
            case "dificil":
                pontos += 20
            case "insana":
                pontos += 25

    if quant_perguntas <= 10:
        gerar_perguntas()
        titulo.config(text=str(ler_vetor_atual["pergunta"]))
        for i in range(0,3,1):
            botao[i].config(text= letras_alternativas[i] + str(puxar_alternativas[i]))
        ponto_escrito.config(text="PONTOS : " + str(pontos))
        return True
    else:
        apaque_bots()
        titulo.config(text="\nFIM DO QUIZ \n\nsua pontuação: " + str(pontos))
        titulo.grid(row=0, column=0, pady=(0, 0))
# =-=-=-=-=-FAZ-O-PRIMEIRO-SORTEIO-=-=-=-=-=
gerar_perguntas()

# =-=-=-=-=-inicia-a-parte-visual-aqui-=-=-=-=-=
aba = Tk()
aba.geometry("1000x800")
aba.title("quiz")
aba.config(background=str(cores[0]))

frame_principal = Frame(aba, bg=str(cores[0]))
frame_principal.pack(expand=True)

fontes()

# =-=-=-=-=-AQUI-É-O-TITULO-=-=-=-=-=
if quant_perguntas > 0 and isinstance(ler_vetor_atual, dict):
    titulo_texto = ler_vetor_atual.get("pergunta", "Pergunta não encontrada")
else:
    titulo_texto = "Selecione a dificuldade do quiz"

titulo = Label(frame_principal, text=titulo_texto)
titulo.config(font=fonte_titulo, foreground=str(cores[1]), bg=str(cores[0]))
titulo.grid(row=0, column=0, pady=(0, 50))
frame_botoes = Frame(frame_principal, bg=str(cores[0]))
frame_botoes.grid(row=1, column=0)

# =-=-=-=-=-AQUI-SÃO-TODOS-OS-BOTÕES-=-=-=-=-=
for i in range(0, 4, 1):
    botao[i] = Button(frame_botoes, text= str(letras_alternativas[i]) + str(puxar_alternativas[i]), width=20, height=5)
    botao[i].config(font=fonte_bot, fg=str(cores[1]), bg=str(cores[2]), command=lambda i=i: pontuacao(i))
    botao[i].grid(row=i, column=0, pady=10, padx=10)

# =-=-=-=-=-PONTUAÇÃO-ESCRITA=-=-=-=-=
ponto_escrito = Label(frame_botoes, font=fonte_ponto, text="PONTOS :" + str(pontos))
ponto_escrito.config(font=fonte_ponto, fg=str(cores[1]), bg=str(cores[0]))
ponto_escrito.grid(row=5, column=0, pady=10, padx=10)

frame_principal.grid_rowconfigure(0, weight=1)
frame_principal.grid_rowconfigure(2, weight=1)
frame_principal.grid_columnconfigure(0, weight=1)

aba.mainloop()
