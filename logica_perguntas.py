import json
import random

class Organiza_Perguntas:
    def __init__(self):
        with open("perguntas.json", "r", encoding="utf-8") as perguntas_json:
            self.perguntas = json.load(perguntas_json)

        self.perguntas_F = self.perguntas["perguntas_F"]
        self.perguntas_M = self.perguntas["perguntas_M"]
        self.perguntas_D = self.perguntas["perguntas_D"]
        self.perguntas_E = self.perguntas["perguntas_E"]

        self.guardar_perguntas_usadas = []
        self.pergunta_atual = 0
        self.quant_perguntas = 0
        self.puxar_alternativas = []
        self.pontos = 0
        self.ler_vetor_atual = {}
        self.ler_erradas_atuais = []
        self.dificuldade = ""

    def dificuldades(self, a):
        match a:
            case 0: return "facil"
            case 1: return "medio"
            case 2: return "dificil"
            case 3: return "insana"

    def sortear_pergunta(self):
        while True:
            indice = random.randint(0, 10)
            if indice not in self.guardar_perguntas_usadas:
                return indice

    def sortear_alternativas(self):
        return random.sample([1, 2, 3, 4], k=4)

    def texto_alternativas(self):
        if self.quant_perguntas == 0:
            self.puxar_alternativas = ["facil", "medio", "dificil", "insana"]
            self.quant_perguntas += 1
        else:
            self.quant_perguntas += 1
            a = random.randint(0, 10)
            match self.dificuldade:
                case "facil":
                    self.ler_vetor_atual = self.perguntas_F[self.pergunta_atual]
                case "medio":
                    self.ler_vetor_atual = self.perguntas_F[self.pergunta_atual] if a < 3 else self.perguntas_M[self.pergunta_atual]
                case "dificil":
                    self.ler_vetor_atual = self.perguntas_M[self.pergunta_atual] if a < 3 else self.perguntas_D[self.pergunta_atual]
                case "insana":
                    self.ler_vetor_atual = self.perguntas_D[self.pergunta_atual] if a < 3 else self.perguntas_E[self.pergunta_atual]

            self.ler_erradas_atuais = self.ler_vetor_atual["erradas"]

            for i in range(len(self.puxar_alternativas)):
                match self.puxar_alternativas[i]:
                    case 1: self.puxar_alternativas[i] = self.ler_vetor_atual["certa"]
                    case 2: self.puxar_alternativas[i] = self.ler_erradas_atuais[0]
                    case 3: self.puxar_alternativas[i] = self.ler_erradas_atuais[1]
                    case 4: self.puxar_alternativas[i] = self.ler_erradas_atuais[2]

        return list(self.puxar_alternativas)

    def gerar_perguntas(self):
        self.pergunta_atual = self.sortear_pergunta()
        self.guardar_perguntas_usadas.append(self.pergunta_atual)
        self.puxar_alternativas = self.sortear_alternativas()
        alternativas_texto = self.texto_alternativas()

        return {
            "quant": self.quant_perguntas,
            "alternativas": alternativas_texto,
            "pontos": self.pontos,
            "pergunta": self.ler_vetor_atual.get("pergunta", "")
        }

    def responder(self, escolha_index):
        """
        Deve ser chamado ao clicar em uma alternativa.
        Retorna um dicionário com o estado atualizado.
        """
        if self.quant_perguntas == 1:
            self.dificuldade = self.dificuldades(escolha_index)
            return self.gerar_perguntas()

        if self.puxar_alternativas[escolha_index] == self.ler_vetor_atual["certa"]:
            match self.dificuldade:
                case "facil": self.pontos += 10
                case "medio": self.pontos += 15
                case "dificil": self.pontos += 20
                case "insana": self.pontos += 25

        if self.quant_perguntas <= 10:
            return self.gerar_perguntas()
        else:
            return {
                "fim": True,
                "pontos": self.pontos
            }
