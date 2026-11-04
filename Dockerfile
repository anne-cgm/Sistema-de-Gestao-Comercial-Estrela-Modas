# Receita da imagem

# Escolhe a imagem base do Python
FROM python:3.14-slim

# Define a pasta de trabalho dentro do container
WORKDIR /app 

#Configura variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

#Copia arquivos do projeto para imagem 
COPY requirements.txt .

#Executa comandos durante a construção
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

# Documenta a porta utilizada pela aplicação
EXPOSE 8000

#Define o comando executado ao iniciar o container 
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]