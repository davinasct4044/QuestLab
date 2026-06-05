# QuestLab

O **QuestLab** é uma plataforma web que utiliza Inteligência Artificial para transformar conteúdos de estudo em avaliações personalizadas.

O usuário informa um tema, resumo ou matéria de interesse, define a quantidade de questões desejada e o sistema gera automaticamente uma prova objetiva para testar seus conhecimentos. Após responder às questões, o usuário recebe seu resultado e percentual de acertos.

---

## Funcionalidades

* Geração automática de provas com Inteligência Artificial
* Definição da quantidade de questões (até 30)
* Questões de múltipla escolha
* Correção automática das respostas
* Exibição do percentual de acertos
* Sistema de autenticação de usuários
* Cadastro e login com senhas protegidas por bcrypt
* Gerenciamento de sessão do usuário

---

## Tecnologias Utilizadas

### Backend

* Python
* Flask
* SQLite
* bcrypt

### Frontend

* HTML5
* CSS3
* JavaScript
* Bootstrap Icons

### Inteligência Artificial

* Groq API
* Llama 3.3 70B Versatile

---

## Segurança

As senhas dos usuários não são armazenadas em texto puro.

O sistema utiliza **bcrypt** para gerar hashes seguros antes do armazenamento no banco de dados, aumentando a proteção das credenciais dos usuários.

---

## 🎯 Objetivo do Projeto

Este projeto foi desenvolvido com o objetivo de praticar:

* Desenvolvimento web com Flask
* Integração com APIs de Inteligência Artificial
* Autenticação e gerenciamento de usuários
* Boas práticas de segurança
* Construção de interfaces modernas e intuitivas

Além disso, o projeto faz parte do meu portfólio de desenvolvimento e demonstra conhecimentos em aplicações web completas (frontend, backend, banco de dados e integração com IA).

---

## Demonstração

### Tela Inicial

<img width="1869" height="920" alt="Captura de tela 2026-06-05 182336" src="https://github.com/user-attachments/assets/962ee41a-5a2e-4210-8aea-7ef1c641a0ba" />

### Geração de Questões

<img width="1854" height="921" alt="Captura de tela 2026-06-05 182403" src="https://github.com/user-attachments/assets/ab64435d-946b-4f93-9b7d-ae069659e4ee" />

### Resultado da Avaliação

<img width="1854" height="920" alt="Captura de tela 2026-06-05 183446" src="https://github.com/user-attachments/assets/a1e4b831-1629-4cf1-a87f-c4096a1f8587" />

---

## ⚙️ Instalação

```bash
git clone https://github.com/davinasct4044/Questlab.git

cd questlab

pip install -r requirements.txt
```

Crie um arquivo `.env`:

```env
GROQ_API_KEY=sua_chave_aqui
```

Execute a aplicação:

```bash
python app.py
```

---

## Licença

Este projeto está licenciado sob a licença MIT.
