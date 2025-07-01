# 📚 BookSync - Backend API

API REST do projeto **BookSync**, um sistema para organização, avaliação e acompanhamento de livros lidos ou em leitura. Desenvolvido com Flask, JWT e integração com a Google Books API.

---

## ✅ Funcionalidades

- 📌 Cadastro e autenticação de usuários com JWT
- 🔐 Proteção de rotas com token Bearer
- 🔍 Pesquisa de livros na Google Books API
- 💾 Salvamento de livros na conta do usuário
- 🌟 Avaliação de livros com:
  - Nota (1 a 5 estrelas)
  - Comentário
  - Status: "lido" ou "lendo"
- ✏️ Edição e exclusão de avaliações
- 🔄 Alteração de status de leitura
- 🧾 Documentação Swagger interativa (`/apidocs`)

---

## ⚙️ Tecnologias utilizadas

- Python 3.11+
- Flask
- Flask-SQLAlchemy
- Flask-JWT-Extended
- Flask-CORS
- Pydantic (validação de entrada)
- Requests (Google Books API)
- SQLite (banco local)

---

## 🚀 Como rodar localmente

### Pré-requisitos

- [Python 3.11+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads)
- (Opcional) Ambiente virtual Python

### Passos

```bash
# Clone o repositório
git clone https://github.com/maiagripp/booksync-api.git
cd booksync-api

# Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate  #macOS/Linux
venv\Scripts\activate #Windows 

# Instale as dependências
pip install -r requirements.txt

# Rode o servidor Flask
flask --app app run
🔗 A API estará disponível em http://localhost:5000
📑 A documentação Swagger pode ser acessada em http://localhost:5000/apidocs/
```

### 📁 Estrutura do projeto
```plaintext
📦 booksync-api
 ┣ 📜 app.py              # Ponto de entrada do Flask
 ┣ 📜 config.py           # Configurações gerais (JWT, DB, CORS)
 ┣ 📜 database.py         # Instância e inicialização do SQLAlchemy
 ┣ 📁 models/             # Modelos ORM: User, Book, UserBook
 ┣ 📁 routes/             # Blueprints organizadas (auth, books)
 ┣ 📁 schemas/            # Schemas de validação com Pydantic
 ┣ 📁 services/           # Integração com Google Books e lógica extra
 ┗ 📜 requirements.txt    # Dependências do projeto
 ```

### 🔐 Segurança
Tokens JWT com expiração

Logout automático no frontend quando o token expira

Proteção das rotas com @jwt_required()

### 🔄 Integração com o Frontend
O frontend (SPA com HTML/CSS/JS) está em outro repositório: [Front](https://github.com/maiagripp/booksync-front)


### 📂 booksync-front
Certifique-se de que ambos os projetos estejam sendo executados com o backend escutando em http://127.0.0.1:5000.

### 📧 Contato
Claudia Maia — [Email-me](mailto:maiaandradec@gmail.com)

Projeto desenvolvido como MVP para pós-graduação em Engenharia de Software - Sprint Desenvolvimento FullStack Básico na PUC-Rio.

