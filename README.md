# BookSync - Backend API

API REST para o projeto BookSync, um sistema web para organização, avaliação e comentário de livros lidos e em leitura.  
O backend é feito em Python com Flask, Flask-SQLAlchemy para o ORM, e integração com a Google Books API para pesquisa de livros.

---

## Funcionalidades

- Cadastro e autenticação de usuários com JWT
- Pesquisa de livros via Google Books API
- Adição de livros favoritos/avaliados por usuário
- Avaliação e comentário sobre livros (nota 1 a 5 e texto)
- Organização básica dos livros do usuário

---

## Tecnologias usadas

- Python 3.11+
- Flask
- Flask-SQLAlchemy
- Flask-JWT-Extended
- Flask-CORS
- Requests (para integração com Google Books)

---

## Como rodar localmente

### Pré-requisitos

- Python 3.11 ou superior instalado
- Banco SQLite (já configurado no projeto)

### Passos

1. Clone o repositório:

```bash
git clone https://github.com/maiagripp/booksync-api.git
cd booksync-api
```

2. Instale as dependências:

```bash
python -m venv .venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

3. Configure variáveis de ambiente

As configs estão em `config.py`.

4. Rode a aplicação:

```bash
flask --app app run
```

O backend estará disponível em `http://localhost:5000`.

---

## Estrutura do projeto

```
/app.py               # arquivo principal do Flask
/config.py            # configurações da aplicação
/database.py          # inicialização do banco com SQLAlchemy
/models/              # modelos de dados (User, Book, UserBook, etc)
/routes/              # rotas agrupadas em Blueprints (auth, book, etc)
/services/            # integração com Google Books e lógica de negócio
/requirements.txt     # dependências do projeto
```

---

## Observações

- Banco usado: SQLite para simplicidade no MVP  
- Autenticação via JWT para segurança nas rotas protegidas  
- Frontend separado, SPA em HTML/CSS/JS puro (em outro repositório/pasta)  

---

## Contato

Claudia Maia — maiaandradec@gmail.com  
Projeto desenvolvido como MVP para pós-graduação em Engenharia de Software - Sprint Desenvolvimento FullStack Básico na PUC-Rio.