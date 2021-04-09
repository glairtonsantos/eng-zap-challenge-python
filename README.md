# Code Challenge Grupo ZAP

No fim de 2017, os dois maiores portais imobiliários do país se fundiram. Esse desafio roda em torno do dia-a-dia do grupo ZAP de integrar as tecnologias e regras de negócio de ambos, de maneira escalável e sustentável, para revolucionar o mercado imobiliário do Brasil.

## Instalação

### Pré Requisitos

- [Python](https://www.python.org/)
- [PIP](https://pip.pypa.io/en/stable/installing/)

### Uso em Desenvolvimento

1. Clone o repositório:
```bash
git clone https://github.com/glairtonsantos/trophy.git
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