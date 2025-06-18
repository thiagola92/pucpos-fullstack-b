# pucpos-fullstack-b
Este é o **backend** do MVP da pós graduação.  

O repositório do **frontend** se encontra em: https://github.com/thiagola92/pucpos-fullstack-f  

# Pré-requisitos

## Debian
Pacotes Debians necessários:  
```
sudo apt install python3.13-venv
```

Criação e ativação do ambiente virtual:  
```
python3 -m venv venv
. venv/bin/activate
```

Instalação de pacotes Pythons necessários:  
```
pip install -r requirements.txt
```

## Windows
Instale [Python](https://www.python.org/) em sua máquina.  

Criação e ativação do ambiente virtual:  
```
python -m venv venv
venv\Scripts\activate
```

Instalação de pacotes Pythons necessários:  
```
pip install -r requirements.txt
```

# Execução
Execute ao menos uma vez a criação do banco de dados:  
```
flask init-db
```
Execuções seguintes irão recria-lo.  

Para execução no modo debug e acesso local:  
```
flask run --debug
```
Acesse por http://127.0.0.1:5000  

# Referencias
- https://docs.sqlalchemy.org/en/20/orm/quickstart.html
- https://flask.palletsprojects.com/en/stable/
- https://luolingchun.github.io/flask-openapi3/
- https://luolingchun.github.io/flask-openapi3/v4.x/Usage/Request/#query