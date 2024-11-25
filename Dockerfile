# Etapa 1: Usar a imagem oficial do Python como base
FROM python:3.9-slim

# Etapa 2: Definir o diretório de trabalho
WORKDIR /app

# Etapa 3: Copiar o arquivo requirements.txt para o contêiner
COPY requirements.txt /app/

# Etapa 4: Instalar as dependências do requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Etapa 5: Copiar o código da aplicação para o contêiner
COPY . /app/

# Etapa 6: Expor a porta que o Flask vai rodar
EXPOSE 8858

# Etapa 7: Comando para rodar a aplicação Flask
CMD ["python", "main.py"]
