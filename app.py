import bcrypt
from flask import Flask, url_for, render_template, request, redirect, session, flash #importa a lib Flask
from questgeneratorAI import create_exam #importa o modulo que cria o questionario
from database import create_table, signup_user, get_user, delete_user, get_user_by_id, update_user
#funcionalidades do banco de dados
import os #modulo para interagir com arquivos
from dotenv import load_dotenv #modulo para interagir com variáveis de ambiente
from json import loads #modulo para interagir com JSON
from bcrypt import checkpw, hashpw, gensalt


app = Flask(__name__)

create_table() #cria uma tabela no banco de dados
load_dotenv() #carrega as funcionalidades do module
app.secret_key = os.getenv('SESSION_KEY') #acessa o arquivo .env

@app.route('/') #tela principal onde o usuário digita o texto para a IA

def render_index():
    return render_template("index.html")

@app.route('/sign-up/<string:routename>', methods=['GET', 'POST'])

#rota para renderizar tela de cadastro e cadastrar usuário no sistema
def sign_up(routename): #recebe o nome da rota para depois que o usuário terminar, redirecioná-lo de volta
    def signup_and_redirect(routename):
        username = request.form['username']
        email = request.form['email'] #pega os dados enviados
        password = request.form['password']

        hashed_password = hashpw( #função do module bcrypt para criptografar as senhas
            password.encode('utf-8'), #transforma senha em bytes
            gensalt() #gera salt aleatório
        ).decode('utf-8') #transforma a hash no tipo string


        signup_user(username, email, hashed_password) #envia os dados enviados como parametros
        # executa a função que interage com o banco de dados, para registrar o usuario

        if routename == 'index':
            return redirect(url_for('render_index')) #redireciona para a rota index

        elif routename == 'exam':
            return redirect(url_for('render_exam')) #redireciona para a rota exam

        elif routename == 'result':
            return redirect(url_for('render_result')) #redireciona para a rota result

    if request.method == 'POST': #verifica se o método é POST
        return signup_and_redirect(routename) #executa a função para cadastrar o usuário


    return render_template('signup.html', routename=routename) #renderiza a página de cadastro

@app.route('/sign-out/<routename>', methods=['POST']) #rota para deslogar usuário

def sign_out(routename): #recebe o nome da rota para depois que o usuário terminar, redirecioná-lo de volta
    session.pop('username', None) # remove o nome do usuario do session

    if routename == 'index':
        return redirect(url_for('render_index')) #redireciona para a rota index
    elif routename == 'exam':
        return redirect(url_for('render_exam')) #redireciona para a rota exam
    elif routename == 'result':
        return redirect(url_for('render_result')) #redireciona para a rota result

@app.route('/login/<routename>', methods=['GET', 'POST']) #rota para logar usuario mostrando tela de login e logando usuario

def login(routename): #recebe o nome da rota para depois que o usuário terminar, redirecioná-lo de volta
    def login_and_redirect(routename):
        useremail = request.form['email'] #pega os dados enviados
        password = request.form['password']

        database_email = get_user(useremail) #guarda o retorno da função que procura no banco de dados o email digitado



        if database_email: #verifica se existe o email
            if checkpw( #verifica se a senha digitada transformada em hash com o salt guardado é igual a senha criptografada
                    password.encode('utf-8'), #transforma a senha digitada pelo usuario em bytes
                    database_email['password'].encode('utf-8') # transforma a senha criptografada salvada de sting em bytes
            ):
                session['username'] = database_email['name']  # define nome no session
                session['id'] = database_email['id']  # define id no session

            else: #se a senha não for igual
                flash('senha incorreta, tente novamente!') #retorna mensagem de erro pro usuario
                return redirect(url_for('login', routename=routename))#redireciona o usuario
        else: #se o email não existir
            flash('usuário não existe!')#retorna a mensagem de erro pro usuario
            return redirect(url_for('login', routename=routename)) #redireciona o usuario

        if routename == 'index':
            return redirect(url_for('render_index')) #redireciona para a rota index
        elif routename == 'exam':
            return redirect(url_for('render_exam')) #redireciona para a rota exam
        elif routename == 'result':
            return redirect(url_for('render_result')) #redireciona para a rota result

    if request.method == 'POST': #verifica se o método é POST
        return login_and_redirect(routename) #executa a função para logar o usuário
    return render_template('login.html', routename=routename) #renderiza a tela de login

@app.route('/delete-account/<routename>/<int:id>', methods=['POST']) #rota representando o Delete do CRUD

def delete_account(routename, id): #recebe o nome da rota para depois que o usuário terminar, redirecioná-lo de volta
    delete_user(id) #executa a função do database.py para deletar usuário do banco de dados
    session.pop('username', None) #tira nome do usuario do session
    session.pop('id', None) #tira o id do usuário do session

    if routename == 'index':
        return redirect(url_for('render_index')) #redireciona para a rota index
    elif routename == 'exam':
        return redirect(url_for('render_exam')) #redireciona para a rota exam
    elif routename == 'result':
        return redirect(url_for('render_result')) #redireciona para a rota result

@app.route('/edit/<routename>', methods=['GET', 'POST'])
#rota responsável pelo Update do CRUD, renderiza a tela e atualiza no banco de dados

def edit_account(routename): #recebe o nome da rota para depois que o usuário terminar, redirecioná-lo de volta
    def change_password(routename):
        old_password = request.form['old_password'] #senha velha
        new_password = request.form['new_password'] #nova senha
        confirm_password = request.form["confirm_password"] #senha do campo confirme senha

        if new_password != confirm_password: #compara se a senha digitada é a mesma do confirme senha
            flash("As senhas não coincidem.") #retorna a mensagem de erro pro usuário
            return redirect(
                url_for("edit_account", routename=routename) #redireciona o usuário pra edit.html
            )

        id = session.get('id') #pega o id do usuario no session
        user = get_user_by_id(id) #guarda o retorno da função que busca o usuario no banco de dados pelo id

        if checkpw( #verifica se a senha digitada transformada em hash com o salt guardado é igual a senha criptografada
            old_password.encode('utf-8'), #transforma a senha digitada pelo usuario em bytes
            user['password'].encode('utf-8') # transforma a senha criptografada salvada de sting em bytes
        ):
            hashed_password = hashpw( #criptografa a nova senha
                new_password.encode('utf-8'), #transforma a nova senha em bytes
                gensalt() #gera o salt
            ).decode('utf-8') #converte a senha criptografada em string
            update_user(id, hashed_password)  # realiza a troca da senha no banco de dados
        else:
            flash('senha incorreta, tente novamente!')  # retorna a mensagem de erro pro usuário
            return redirect(url_for('edit_account', routename=routename))

        if routename == 'index':
            return redirect(url_for('render_index')) #redireciona para a rota index
        elif routename == 'exam':
            return redirect(url_for('render_exam')) #redireciona para a rota exam
        elif routename == 'result':
            return redirect(url_for('render_result')) #redireciona para a rota result
    if request.method == 'POST': #verifica se o método é POST
        return change_password(routename) #executa a função para trocar a senha do usuário

    return render_template('edit.html', routename=routename) #renderiza a tela de troca de senha

@app.route('/generating_exam' , methods=['POST']) #IA gera as questões → redireciona pra /exam
def generate_exam():
    contentUser = request.form['inputcontent'] #guarda o conteúdo digitado pelo usuário

    if not contentUser.strip(): #verifica se o usuário enviou sem conteúdo
        flash("Digite algum conteúdo para gerar a prova.") #retorna mensagem de erro pro usuário
        return redirect(url_for("render_index"))

    questions_quantity = int(request.form["questions_quantity"]) #pega a quantidade de questões desejada

    if questions_quantity > 30: #verifica se o usuário enviou mais de 30 questões
        flash("O limite máximo é de 30 questões.")
        return redirect(url_for("render_index"))

    quest_generated = create_exam(contentUser,questions_quantity) #guarda a resposta da IA

    try:
        quest_generated = loads(quest_generated) #tenta ler o JSON retornado
    except Exception as e: #se der algum erro
        flash('erro ao gerar prova, tente novamente!') #retorna a mensagem de erro pro usuário
        return redirect(url_for('render_index'))

    if "erro" in quest_generated: #retorna erro se a IA enviar erro por não conseguir gerar prova
        flash(quest_generated["erro"]) #retorna mensagem de erro pro usuário
        return redirect(url_for('render_index')) #redireciona o usuario de volta

    quest_generated = dict( #ordena as questões em ordem numérica
        sorted(
            quest_generated.items(),
            key=lambda item: int(item[0].split('_')[1])
        )
    )

    session['quest_generated'] = quest_generated #guarda o questionário gerado no session.
    return redirect(url_for('render_exam')) #manda o usuário para a rota que renderiza o simulado

@app.route('/exam' , methods=['GET']) #exibe o questionário

def render_exam():
    quest = session.get('quest_generated') #pega o questionário do session
    return render_template('exam.html', questoes=quest) #renderiza o questionário


@app.route('/generating_result', methods=['POST']) #mostra quantas acertou

def generate_result():
    quest = session.get('quest_generated') #pega o questionário no session
    client_answers = request.form.to_dict() #pega as respostas do usuário vindas do formulário como dict

    if len(client_answers) != len(quest): #verifica se a quantidade de questões é diferente da quantidade de questões respondidadas
        flash('responda todas as questões antes de enviar!') #retorna mensagem de erro pro usuário
        return render_template('exam.html', questoes=quest, client_answers=client_answers)
        #renderiza o resultado

    correct_answers = 0 #quantas questões o usuário acertou
    correct_questions = dict() #quais alternativas das questões o usuário acertou

    for key, value in client_answers.items(): #itera as respostas que o usuario respondeu por chave e valor
        correct_questions[key] = quest[key]['resposta_correta'] #guarda na chave do correct_questions a alternativa certa
        if value == quest[key]['resposta_correta']: #verifica se a resposta do usuário e a resposta certa são iguais
            correct_answers += 1 #soma mais um no correct_answers
    session['correct_answers'] = correct_answers #guarda quantas questões o usuário acertou no session
    session['correct_questions'] = correct_questions
    # guarda quais alternativas das questões o usuário acertou no session
    return redirect(url_for('render_result'))


@app.route('/result', methods=['GET']) #renderiza a tela de resultado
def render_result():
    questions = session.get('correct_questions') #pega o questionário no session
    questions_quantity = len(questions) #guarda quantas questões tem o questionário
    result = session.get('correct_answers') # pega no session quantas questões o usuário acertou
    porcentage = result * 100 / len(questions) #calcula a porcentagem de acerto do usuário
    if session.get('username'): #verifica se tem usuário logado
        user = session.get('username') #guarda o nome do usuário logado
        return render_template('result.html', result=result, porcentage=porcentage,
                               questions_quantity=questions_quantity, username=user) #renderiza a tela
    return render_template('result.html', result=result, porcentage=porcentage, questions_quantity=questions_quantity)
    # renderiza a tela
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000, debug=True) #roda a aplicação
