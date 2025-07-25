from logica_quiz import Organiza_Perguntas

self.quiz = Organiza_Perguntas()

# Exemplo ao iniciar o quiz
dados = self.quiz.gerar_perguntas()
print(dados["pergunta"])
print(dados["alternativas"])

# Exemplo ao clicar em uma alternativa
dados = self.quiz.responder(indice_escolhido)
if "fim" in dados:
    print("Fim do quiz!")
else:
    print(dados["pergunta"], dados["pontos"])
