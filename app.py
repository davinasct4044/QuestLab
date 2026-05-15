from flask import Flask #importa a lib Flask
from questgeneratorAI import create_exam #importa o modulo que cria o questionario

app = Flask(__name__)


@app.route('/') #tela principal onde o usuário digita o texto para a IA
def render_input():
    print()
@app.route('/generating_exam' , methods=['POST'])#IA gera as questões → redireciona pra /exam
def generate_exam():
    print()
@app.route('/exam' , methods=['GET'])#exibe o questionário
def hello_world():
    print()

@app.route('/result', methods=['GET']) #mostra quantas acertou
def result():
    print()


if __name__ == '__main__':
    app.run()
