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
pip install Flask flask-openapi3[swagger]
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
pip install Flask flask-openapi3[swagger]
```

# Execução
Para execução no modo debug:  
```
flask run --debug
```
