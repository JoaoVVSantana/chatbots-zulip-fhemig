# Use uma imagem base oficial do Python
FROM python:3.9-slim

# Configura a variável de ambiente para desativar buffers (melhor para logs em Docker)
ENV PYTHONUNBUFFERED 1

# Define o diretório de trabalho no contêiner
WORKDIR /app

# Copia o arquivo de dependências (requirements.txt)
COPY requirements.txt /app/

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia todos os arquivos do projeto para o contêiner
COPY . /app/

# Expõe a porta caso necessário (exemplo: 5000 ou outra porta)
EXPOSE 5000

# Define o comando para iniciar o bot
CMD ["python", "main.py"]
