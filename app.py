from flask import Flask, url_for, render_template, request, redirect, session #importa a lib Flask
from questgeneratorAI import create_exam #importa o modulo que cria o questionario
import os
from dotenv import load_dotenv
from json import loads

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
    quest_generated = dict(
        sorted(
            quest_generated.items(),
            key=lambda item: int(item[0].split('_')[1])
        )
    )
    session['quest_generated'] = quest_generated
    return redirect(url_for('render_exam'))

@app.route('/exam' , methods=['GET'])#exibe o questionário
def render_exam():
    quest = session.get('quest_generated')

    return render_template('exam.html', questoes=quest)

@app.route('/generating_result', methods=['POST']) #mostra quantas acertou
def generate_result():
    client_answers = request.form.to_dict()
    quest = session.get('quest_generated')
    correct_answers = 0
    correct_questions = dict()

    for key, value in client_answers.items():
        correct_questions[key] = quest[key]['resposta_correta']
        if value == quest[key]['resposta_correta']:
            correct_answers += 1
    session['correct_answers'] = correct_answers
    session['correct_questions'] = correct_questions



    return redirect(url_for('render_result'))


@app.route('/result', methods=['GET'])
def render_result():
    questions = session.get('correct_questions')
    questions_quantity = 0
    for key in questions:
        questions_quantity += 1
    result = session.get('correct_answers')
    porcentage = result * 100 / len(questions)
    return render_template('result.html', result=result, porcentage=porcentage, questions_quantity=questions_quantity)
if __name__ == '__main__':
    app.run()
