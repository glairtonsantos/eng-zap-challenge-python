# Code Challenge Grupo ZAP

No fim de 2017, os dois maiores portais imobiliários do país se fundiram. Esse desafio roda em torno do dia-a-dia do grupo ZAP de integrar as tecnologias e regras de negócio de ambos, de maneira escalável e sustentável, para revolucionar o mercado imobiliário do Brasil.

## Acesse a versão no Heroku
`https://eng-zap-challenge-python.herokuapp.com/`

*OBS: Pode haver demora no primeiro acesso por conta que o heroku está iniciando o servidor caso ele estiver ocioso*
## Instalação

### Pré Requisitos

- [Python](https://www.python.org/)
- [PIP](https://pip.pypa.io/en/stable/installing/)

### Uso Local

1. Clone o repositório:
```bash
git clone https://github.com/glairtonsantos/eng-zap-challenge-python.git
```
2. Crie um ambiente virtual para as depedências:

Algumas opções para fazer isso são:
- [venv](https://docs.python.org/3/library/venv.html)
- [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/)
- [virtualenv](https://virtualenv.pypa.io/en/latest/)

Exemplo com `virtualenv`
```bash
python -m pip install --user virtualenv
```
**obs: em algumas instalações é necessário utilizar `python3` ou `pip3` no comando*

depois crie um ambiente virtual
```bash
virtualenv nome_da_virtualenv
```

após criar uma `virtualenv` basta ativar
```bash
source nome_da_virtualenv/bin/activate
```

3. Instale as depedências

acesse a pasta do arquivo `requirements-dev.txt` e execute o comando (com a `virtualenv` ativada)
```bash
pip install -r requirements-dev.txt
```

para verificar as depedências instaladas basta executar
```bash
pip freeze
```

4. Executar localhost

agora com tudo instalado execute o comando
```bash
python app.py runserver
```
ou
```bash
flask run
```

se tudo der certo vai exibir a seguinte mensagem:
```
WARNING:root:wait...load source from http://grupozap-code-challenge.s3-website-us-east-1.amazonaws.com/sources/source-2.json
INFO:werkzeug: * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```
basta acessar `http://127.0.0.1:5000/` no seu navegador ou algum `API clients` etc.

## Utilizando

### Endpoints

| Method | Endpoint                | Descrição                                                            |
| :----: | ----------------------- | ------------------------------------------------------------------   |
| `GET`  | `/`                     | Informações da API                                                   |
| `GET`  | `/properties/<portal>/` | Lista os imóveis de acordo com o portal informado <zap, viva-real>   |


### Parametros (opcionais) da URL

| query params  | Type | Descrição                            |
| :------------:| -----| ------------------------------------ |
| `?page=`      | int  | número página que deseja listar      |
| `?page_size=` | int  | quantidade de elementos por pagina   |

#### exemplos

```
GET http://127.0.0.1:5000/properties/zap/?page=5&page_size=10
```

```
GET http://127.0.0.1:5000/properties/viva-real/?page=10&page_size=5
```


## Executando os Testes

execute o comando
```bash
python -m pytest -v
```

para obter relatório de cobertura
```bash
python -m pytest --cov=eng_zap_challenge_python  tests/
```

para export o relatório em html
```
python -m pytest --cov eng_zap_challenge_python/ --cov-report html
```
após executar esse comando uma pasta `htmlcov/` será criada e basta acessar e clicar no arquivo `index.html`


## Como Publicar

*OBS: Esse tutorial é para o `Gunicorn`, para o servidor `Apache` com `mod_wsgi` é necessário outros passos. [verifique aqui](https://flask.palletsprojects.com/en/1.1.x/deploying/mod_wsgi/)*

Siga os passos da instalação local até o **passo 3** mas mude para o arquivo `requirements.txt`

3. Instale as depedências

acesse a pasta do arquivo `requirements.txt` e execute o comando (com a `virtualenv` ativada)

```bash
pip install -r requirements.txt
```

4. Servindo a aplicação

*OBS: é recomendado utilizar [Nginx](https://www.nginx.com/resources/wiki/start/topics/tutorials/install/)*

```
gunicorn --bind 0.0.0.0:5000 wsgi:app
```

*OBS: Considere utilizar um serviço de supervisor para garantir que o **gunicorn** seja executado quando o servidor reiniciar ou em caso de falha, para saber mais [clique aqui](http://supervisord.org/running.html)*

### Saiba mais:

- Deploy [Digital Ocean](https://www.digitalocean.com/community/tutorials/how-to-deploy-a-flask-app-using-gunicorn-to-app-platform)
- Deploy AWS [Elastic Beanstalk](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-flask.html)
- Deploy AWS [EC2](https://medium.com/innovation-incubator/deploy-a-flask-app-on-aws-ec2-d1d774c275a2)
- Deploy serverless Lambda [Zappa](https://docs.aws.amazon.com/pt_br/xray/latest/devguide/xray-sdk-python-serverless.html)