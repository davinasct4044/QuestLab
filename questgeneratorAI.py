from groq import Groq #importando o módulo da API de IA
from dotenv import load_dotenv #modulo nativo para carregar variavel de ambiente .env
import os #modulo nativo para acessar o sistema operacional

load_dotenv()#usa o módulo para carregar as variaveis de ambiente
api_key = os.getenv("GROQ_API_KEY") #pega a key da API na variavel de ambiente e atribui a variavel
client = Groq(api_key=api_key) #acessa a API com a key e atribui para a variavel client

def create_exam(content): #cria a função que vai criar o questionário
    chat_completion = client.chat.completions.create( #acessa a API para criar a conclusão da IA
        messages=[
            {
                "role": "system",
                "content": """Você é um criador de provas especialista, você deverá receber o conteúdo
                 do usuário e assim que receber, crie uma prova usando o conteúdo fornecido, retornando
                 para mim no formato JSON, segue um exemplo:
                    {
                    "questao_1": {
                        "enunciado": "enunciado da questao junto com a pergunta",
                        "alternativas": {
                            "a": "a)texto da alternativa a...",
                            "b": "b)texto da alternativa b...",
                            "c": "c)texto da alternativa c...",
                            "d": "d)texto da alternativa d...",
                            "e": "e)texto da alternativa e..."
                        },
                        "resposta_correta": "a"
                    },
                    "questao_2": {
                        "enunciado": "enunciado da questao + pergunta",
                        "alternativas": {
                            "a": "a)texto da alternativa a...",
                            "b": "b)texto da alternativa b...",
                            "c": "c)texto da alternativa c...",
                            "d": "d)texto da alternativa d...",
                            "e": "e)texto da alternativa e..."
                        },
                        "resposta_correta": "a"
                    }
                  }
                  Apenas um exemplo, mas siga a estrutura. E lembre-se você é especialista, não erre.
                  E se o usuário enviar um texto que seja inviável para realizar a prova,
                  retorne a seguinte mensagem: Não foi possível gerar o teste, informações invalidas ou insuficientes.""",
            }, #dictionary onde define comportamento da IA e menciona que é algo do sistema não um prompt do client
            {
                "role": "user",
                "content": content
            }#onde a IA vai receber o prompt do client, coloco para receber o parâmetro que vai ser o conteudo que o cliente forneceu
        ],
        model="llama-3.3-70b-versatile", #modelo da IA
    )
    return chat_completion.choices[0].message.content #retorna o questionário feito pela IA