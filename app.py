from flask import Flask, url_for, render_template, request, redirect, session #importa a lib Flask
from questgeneratorAI import create_exam #importa o modulo que cria o questionario
import os
from dotenv import load_dotenv
from json import load, loads

app = Flask(__name__)

load_dotenv()
app.secret_key = os.getenv('SESSION_KEY') 

@app.route('/') #tela principal onde o usuário digita o texto para a IA
def render_index():
    return render_template("index.html")
@app.route('/generating_exam' , methods=['POST'])#IA gera as questões → redireciona pra /exam
def generate_exam():
    contentUser = request.form['inputcontent']
    quest_generated = create_exam(contentUser)
    quest_generated = loads(quest_generated)
    session['quest_generated'] = quest_generated
    return redirect(url_for('render_exam'))

@app.route('/exam' , methods=['GET'])#exibe o questionário
def render_exam():
    quest = session.get('quest_generated')
    print(quest)
    return render_template('exam.html', questoes=quest)

@app.route('/result', methods=['GET']) #mostra quantas acertou
def result():
    print()


if __name__ == '__main__':
    app.run()
