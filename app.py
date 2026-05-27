from flask import Flask, url_for, render_template, request, redirect, session, flash #importa a lib Flask
from questgeneratorAI import create_exam #importa o modulo que cria o questionario
from database import create_table, signup_user, get_user, delete_user, get_user_by_id, update_user
import os
from dotenv import load_dotenv
from json import loads

app = Flask(__name__)

create_table()
load_dotenv()
app.secret_key = os.getenv('SESSION_KEY')

@app.route('/') #tela principal onde o usuário digita o texto para a IA
def render_index():
    return render_template("index.html")

@app.route('/sign-up/<string:routename>', methods=['GET', 'POST'])
def sign_up(routename):
    def signup_and_redirect(routename):
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        signup_user(username, email, password)

        if routename == 'index':
            return redirect(url_for('render_index'))
        elif routename == 'exam':
            return redirect(url_for('render_exam'))
        elif routename == 'result':
            return redirect(url_for('render_result'))
    if request.method == 'POST':
        return signup_and_redirect(routename)


    return render_template('signup.html', routename=routename)

@app.route('/sign-out/<routename>', methods=['POST'])
def sign_out(routename):
    session.pop('username', None)


    if routename == 'index':
        return redirect(url_for('render_index'))
    elif routename == 'exam':
        return redirect(url_for('render_exam'))
    elif routename == 'result':
        return redirect(url_for('render_result'))

@app.route('/login/<routename>', methods=['GET', 'POST'])
def login(routename):
    def login_and_redirect(routename):
        useremail = request.form['email']
        password = request.form['password']
        database_email = get_user(useremail)
        if database_email:
            if password == database_email['password']:
                session['username'] = database_email['name']
                session['id'] = database_email['id']
            else:
                flash('senha incorreta, tente novamente!')
                return redirect(url_for('login', routename=routename))
        else:
            flash('usuário não existe!')
            return redirect(url_for('login', routename=routename))
        if routename == 'index':
            return redirect(url_for('render_index'))
        elif routename == 'exam':
            return redirect(url_for('render_exam'))
        elif routename == 'result':
            return redirect(url_for('render_result'))

    if request.method == 'POST':
        return login_and_redirect(routename)
    return render_template('login.html', routename=routename)

@app.route('/delete-account/<routename>/<int:id>', methods=['POST'])
def delete_account(routename, id):
    delete_user(id)
    session.pop('username', None)
    session.pop('id', None)


    if routename == 'index':
        return redirect(url_for('render_index'))
    elif routename == 'exam':
        return redirect(url_for('render_exam'))
    elif routename == 'result':
        return redirect(url_for('render_result'))

@app.route('/edit/<routename>', methods=['GET', 'POST'])
def edit_account(routename):
    def change_password(routename):
        old_password = request.form['old_password']
        new_password = request.form['new_password']
        id = session.get('id')
        user = get_user_by_id(id)
        if old_password == user['password']:
            update_user(id, new_password)
        else:
            flash('senha incorreta, tente novamente!')

        if routename == 'index':
            return redirect(url_for('render_index'))
        elif routename == 'exam':
            return redirect(url_for('render_exam'))
        elif routename == 'result':
            return redirect(url_for('render_result'))
    if request.method == 'POST':
        return change_password(routename)

    return render_template('edit.html', routename=routename)
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
    if session.get('username') != False:
        user = session.get('username')
        return render_template('result.html', result=result, porcentage=porcentage,
                               questions_quantity=questions_quantity, username=user)
    return render_template('result.html', result=result, porcentage=porcentage, questions_quantity=questions_quantity)
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000, debug=True)
