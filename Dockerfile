FROM python:3.11-slim

WORKDIR /app

# Instala dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copia requirements e instala dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o backend
COPY . .

# Expõe porta do Flask
EXPOSE 5000

# Comando de produção
CMD ["flask", "--app", "app", "run", "--host=0.0.0.0"]
