import tkinter.font
import json
from tkinter import *
import random

class Quiz:
    def __init__(self):
        # --- perguntas salvas no json ---
        with open("perguntas.json", "r", encoding="utf-8") as perguntas_json:
            self.perguntas = json.load(perguntas_json)

        # ---variaveis-dos-botoes---
        self.perguntas_F = self.perguntas["perguntas_F"]
        self.perguntas_M = self.perguntas["perguntas_M"]
        self.perguntas_D = self.perguntas["perguntas_D"]
        self.perguntas_E = self.perguntas["perguntas_E"]

        self.cores = ["#2E3A59", "#F5F7FA", "#627D98", "#9FB3C8", "#1B4965"]
        self.botao = [0, 1, 2, 3]
        self.letras_alternativas = ["A ", "B ", "C ", "D "]

        # ---variaveis-que-guardam-dados---
        self.guardar_perguntas_usadas = []
        self.pergunta_atual = 0
        self.quant_perguntas = 0
        self.puxar_alternativas = []
        self.pontos = 0
        self.fonte_titulo, self.fonte_bot, self.fonte_ponto = 0, 0, 0
        self.ler_vetor_atual = []
        self.ler_erradas_atuais = []
        self.dificuldade = 0
        self.titulo = 0
        self.ponto_escrito = 0
        self.sair_inicio = False

        # Inicia sorteio inicial
        self.gerar_perguntas()

        # Inicia a parte visual
        self.aba = Tk()
        self.aba.geometry("1000x800")
        self.aba.title("quiz")
        self.aba.config(background=str(self.cores[0]))

        if self.sair_inicio == False:
            self.tela_inicio()
        else:
            self.tela_perguntas()

        self.aba.mainloop()

    def gerar_perguntas(self):
        '''
        essa função junta outras funções da classe no que resulta em
        Sorteiar uma nova pergunta não utilizada,
        adiciona à lista de usadas e prepara as alternativas
        embaralhadas com os textos corretos e errados
        '''
        self.pergunta_atual = self.sortear_pergunta()
        self.guardar_perguntas_usadas.append(self.pergunta_atual)
        self.puxar_alternativas = list(self.sortear_alternativas())
        self.puxar_alternativas = self.texto_alternativas()

    def dificuldades(self, a):
        '''essa função é responsavel por retornar a dificuldade do quiz'''
        match a:
            case 0:
                return "facil"
            case 1:
                return "medio"
            case 2:
                return "dificil"
            case 3:
                return "insana"

    def apaque_bots(self):
        '''essa funço apaga os botões do quiz quando chamada'''
        self.ponto_escrito.destroy()
        for i in range(len(self.botao)):
            self.botao[i].destroy()
        del (self.botao)

    def fontes(self):
        '''função que guarda as fontes'''
        self.fonte_titulo = tkinter.font.Font(family="Comic Sans MS", size=22, weight="bold")
        self.fonte_bot = tkinter.font.Font(family="arial", size=13, weight="bold")
        self.fonte_ponto = tkinter.font.Font(family="arial", size=10)

    def sortear_pergunta(self):
        '''
        Sorteia uma pergunta ainda não usada, registra-a como utilizada e prepara
        as alternativas embaralhadas, substituindo números pelos textos corretos
        e incorretos correspondentes.
        '''
        sortea_indice = random.randint(0, 10)
        if (sortea_indice not in self.guardar_perguntas_usadas):
            return sortea_indice
        else:
            while True:
                sortea_indice = random.randint(0, 10)
                if sortea_indice not in self.guardar_perguntas_usadas:
                    return sortea_indice

    def sortear_alternativas(self):
        '''
        Gera uma lista com os números 1 a 4 em ordem aleatória,
        que representam as posições das alternativas A, B, C e D.
        Esses números serão usados para substituir as alternativas
        na ordem embaralhada a ser exibida ao usuário.
        '''
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

    def texto_alternativas(self):
        """
        Atualiza as alternativas da pergunta atual substituindo os números
        pelas respostas corretas e incorretas conforme a dificuldade escolhida.
        Na primeira rodada, retorna as opções de dificuldade.
        """
        if self.quant_perguntas == 0:
            self.puxar_alternativas = ["facil", "medio", "dificil", "insana"]
            self.quant_perguntas += 1
        else:
            a = 0
            self.quant_perguntas += 1
            match self.dificuldade:
                case "facil":
                    self.ler_vetor_atual = self.perguntas_F[self.pergunta_atual]
                case "medio":
                    a = random.randint(0, 10)
                    if (a < 3):
                        self.ler_vetor_atual = self.perguntas_F[self.pergunta_atual]
                    else:
                        self.ler_vetor_atual = self.perguntas_M[self.pergunta_atual]

                case "dificil":
                    a = random.randint(0, 10)
                    if (a < 3):
                        self.ler_vetor_atual = self.perguntas_M[self.pergunta_atual]
                    else:
                        self.ler_vetor_atual = self.perguntas_D[self.pergunta_atual]
                case "insana":
                    a = random.randint(0, 10)
                    if (a < 3):
                        self.ler_vetor_atual = self.perguntas_D[self.pergunta_atual]
                    else:
                        self.ler_vetor_atual = self.perguntas_E[self.pergunta_atual]

            self.ler_erradas_atuais = self.ler_vetor_atual["erradas"]

            for i in range(0, len(self.puxar_alternativas), 1):
                match self.puxar_alternativas[i]:
                    case 1:
                        self.puxar_alternativas[i] = self.ler_vetor_atual["certa"]
                    case 2:
                        self.puxar_alternativas[i] = self.ler_erradas_atuais[0]
                    case 3:
                        self.puxar_alternativas[i] = self.ler_erradas_atuais[1]
                    case 4:
                        self.puxar_alternativas[i] = self.ler_erradas_atuais[2]
        return list(self.puxar_alternativas)

    def pontuacao(self, a):
        """
        Atualiza a pontuação com base na resposta do usuário,
        gerencia a dificuldade, exibe a próxima pergunta ou finaliza o quiz
        exibindo a pontuação total ao fim das perguntas.
        """
        print(a)
        if self.quant_perguntas == 1:
            self.dificuldade = self.dificuldades(a)
            print(self.dificuldade)
            self.gerar_perguntas()
            self.titulo.config(text=str(self.ler_vetor_atual["pergunta"]))
            for i in range(0, 4, 1):
                self.botao[i].config(text=self.letras_alternativas[i] + str(self.puxar_alternativas[i]))
            self.ponto_escrito.config(text="PONTOS : " + str(self.pontos))
            return

        if self.puxar_alternativas[a] == self.ler_vetor_atual["certa"]:
            match self.dificuldade:
                case "facil":
                    self.pontos += 10
                case "medio":
                    self.pontos += 15
                case "dificil":
                    self.pontos += 20
                case "insana":
                    self.pontos += 25

        if self.quant_perguntas <= 10:
            self.gerar_perguntas()
            self.titulo.config(text=str(self.ler_vetor_atual["pergunta"]))
            for i in range(0, 4, 1):
                self.botao[i].config(text=self.letras_alternativas[i] + str(self.puxar_alternativas[i]))
            self.ponto_escrito.config(text="PONTOS : " + str(self.pontos))
            return True
        else:
            self.apaque_bots()
            self.titulo.config(text="\nFIM DO QUIZ \n\nsua pontuação: " + str(self.pontos))
            self.titulo.grid(row=0, column=0, pady=(0, 0))

    def tela_inicio(self):
        """
        Cria e exibe a tela inicial do quiz com título e botão
        para iniciar o jogo
        """
        self.fontes()

        frame_inicial = Frame(self.aba, bg=self.cores[0])
        frame_inicial.pack(expand=True, fill='both')

        frame_tela_inicial_titulo = Frame(frame_inicial, bg=self.cores[0])
        frame_tela_inicial_titulo.pack(side='top', fill='x', pady=50)

        titulo_inicio = Label(frame_tela_inicial_titulo, text="Bem Vindo ao Quiz")
        titulo_inicio.config(font=self.fonte_titulo, fg=self.cores[1], bg=self.cores[0])
        titulo_inicio.pack()

        frame_tela_inicial_botao = Frame(frame_inicial, bg=self.cores[2])
        frame_tela_inicial_botao.pack(expand=True)

        botao_inicial = Button(frame_tela_inicial_botao, text="Iniciar Quiz", width=25, height=5)
        botao_inicial.config(font=self.fonte_bot, bg=self.cores[2], fg=self.cores[1], command=self.troca_tela)
        botao_inicial.pack()

    def troca_tela(self):
        """
        essa função troca a tela inicial para a tela de perguntas
        """
        self.sair_inicio = True
        for widget in self.aba.winfo_children():
            widget.destroy()
        self.tela_perguntas()
    def tela_perguntas(self):
        """
        Monta a interface da tela de perguntas, exibindo o enunciado,
        botões para as alternativas e a pontuação atualizada.
        """
        frame_principal = Frame(self.aba, bg=str(self.cores[0]))
        frame_principal.pack(expand=True)

        self.fontes()

        if self.quant_perguntas > 0 and isinstance(self.ler_vetor_atual, dict):
            titulo_texto = self.ler_vetor_atual.get("pergunta", "Pergunta não encontrada")
        else:
            titulo_texto = "Selecione a dificuldade do quiz"

        self.titulo = Label(frame_principal, text=titulo_texto)
        self.titulo.config(font=self.fonte_titulo, foreground=str(self.cores[1]), bg=str(self.cores[0]))
        self.titulo.grid(row=0, column=0, pady=(0, 50))

        frame_botoes = Frame(frame_principal, bg=str(self.cores[0]))
        frame_botoes.grid(row=1, column=0)

        for i in range(0, 4, 1):
            self.botao[i] = Button(frame_botoes, text=str(self.letras_alternativas[i]) + str(self.puxar_alternativas[i]), width=20,
                              height=5)
            self.botao[i].config(font=self.fonte_bot, fg=str(self.cores[1]), bg=str(self.cores[2]), command=lambda i=i: self.pontuacao(i))
            self.botao[i].grid(row=i, column=0, pady=10, padx=10)

        self.ponto_escrito = Label(frame_botoes, font=self.fonte_ponto, text="PONTOS :" + str(self.pontos))
        self.ponto_escrito.config(font=self.fonte_ponto, fg=str(self.cores[1]), bg=str(self.cores[0]))
        self.ponto_escrito.grid(row=5, column=0, pady=10, padx=10)

        frame_principal.grid_rowconfigure(0, weight=1)
        frame_principal.grid_rowconfigure(2, weight=1)
        frame_principal.grid_columnconfigure(0, weight=1)


if __name__ == "__main__":
    quiz = Quiz()
