# 📚 BookSync - Backend API

API REST do projeto **BookSync**, desenvolvida para gerenciar usuários, autenticação e a persistência de livros e avaliações. Atua como um **API Gateway** para consumo seguro da Google Books API.

---

## 🏛️ Arquitetura do Projeto

O projeto segue a arquitetura de **Cenário 1.1 (Integração Backend)**. A API atua como intermediária, recebendo requisições do Frontend, consultando o banco de dados local ou a API externa, e tratando os dados antes da resposta.

![Arquitetura do Projeto BookSync](/assets/architeture.png)

*(O consumo da API externa é encapsulado no Backend, garantindo que chaves de API e tratamento de dados fiquem isolados do cliente).*

---

## 🌐 API Externa Utilizada

O sistema consome dados da **Google Books API** para buscar informações de livros (título, autor, capa).

- **Serviço:** Google Books API v1
- **Status:** Pública e Gratuita.
- **Integração:** Feita via biblioteca `requests` no Python.
- **Tratamento:** O Backend recebe o JSON bruto do Google, filtra apenas os campos necessários (título, autores, thumbnail, ID) e entrega um JSON limpo para o Frontend.
- **Rotas Internas que chamam a externa:**
  - `GET /user/books/search?query={termo}`

---

## ⚙️ Tecnologias Utilizadas

- **Linguagem:** Python 3.11+
- **Framework:** Flask
- **Banco de Dados:** SQLite (via Flask-SQLAlchemy)
- **Autenticação:** JWT (Flask-JWT-Extended)
- **Documentação:** Swagger (Flasgger)
- **Containerização:** Docker

---

## ✅ Funcionalidades (Endpoints)

A API fornece 4 métodos HTTP principais:

- **POST** (`/register`, `/login`, `/user/books/{id}`): Cadastro, Autenticação e Salvamento de livros.
- **GET** (`/user/books`, `/user/books/search`): Listagem da estante e busca externa.
- **PUT** (`/user/books/{id}`): Edição de nota, comentário e status.
- **DELETE** (`/user/books/{id}`): Remoção de livro da estante.

> A documentação interativa completa (Swagger) está disponível em `/apidocs` quando a aplicação está rodando.

---

## 🚀 Como Rodar o Projeto

### Pré-requisitos
- [Docker](https://www.docker.com/) OU Python 3.11+ instalado.

### Opção 1: Rodar com Docker 🐳

Para rodar a API isoladamente em um container:

1. Construa a imagem:
```Bash
docker build -t booksync-api .
```
Execute o container:
```Bash
docker run -p 5000:5000 booksync-api
```
A API estará disponível em: http://localhost:5000

Nota: Para rodar o sistema completo (Front + Back), utilize o docker-compose.yml presente no repositório do Frontend.

### Opção 2: Rodar Localmente (Python)
Clone o repositório:
```Bash
git clone https://github.com/maiagripp/booksync-api.git
cd booksync-api
```

Crie e ative o ambiente virtual:

```Bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

Instale as dependências:
```Bash
pip install -r requirements.txt
``` 

Execute a aplicação:

```Bash
flask --app app run
```

📁 Estrutura de Arquivos
```Plaintext
📦 booksync-api
 ┣ 📂 assets/             # Imagens da documentação
 ┃ ┗ 📜 architecture.png  # Diagrama da arquitetura
 ┣ 📁 models/             # Modelos do Banco de Dados (User, UserBook)
 ┣ 📁 routes/             # Rotas da API (Auth, Books)
 ┣ 📁 services/           # Lógica de integração com Google Books
 ┣ 📜 app.py              # Ponto de entrada da aplicação
 ┣ 📜 config.py           # Configurações de ambiente
 ┣ 📜 Dockerfile          # Configuração da imagem Docker
 ┗ 📜 requirements.txt    # Dependências do Python
```

📧 Contato
Claudia Maia — Email-me

Projeto desenvolvido como MVP para pós-graduação em Engenharia de Software - Sprint Desenvolvimento FullStack Básico na PUC-Rio.