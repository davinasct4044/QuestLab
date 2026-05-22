from flask import Flask, url_for, render_template, request, redirect, session, flash #importa a lib Flask
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
    try:
        quest_generated = loads(quest_generated)
    except Exception as e:
        print(f'erro ao converter JSON: {e}')
        flash('erro ao gerar prova, tente novamente!')
        return redirect(url_for('render_index'))
    quest_generated = dict(
        sorted(
            quest_generated.items(),
            key=lambda item: int(item[0].split('_')[1])
        )
    )
    print(quest_generated)
    session['quest_generated'] = quest_generated
    return redirect(url_for('render_exam'))

@app.route('/exam' , methods=['GET'])#exibe o questionário
def render_exam():
    quest = session.get('quest_generated')

    return render_template('exam.html', questoes=quest)

@app.route('/generating_result', methods=['POST']) #mostra quantas acertou
def generate_result():
    quest = session.get('quest_generated')
    client_answers = request.form.to_dict()
    if len(client_answers) != len(quest):
        flash('responda todas as questões antes de enviar!')
        return render_template('exam.html', questoes=quest, client_answers=client_answers)

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
    questions_quantity = len(questions)
    result = session.get('correct_answers')
    porcentage = result * 100 / len(questions)
    return render_template('result.html', result=result, porcentage=porcentage, questions_quantity=questions_quantity)
if __name__ == '__main__':
    app.run()
