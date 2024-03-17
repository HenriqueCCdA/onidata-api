# onidata-api

[![Backend](https://github.com/HenriqueCCdA/onidata-api/actions/workflows/CI.yml/badge.svg)](https://github.com/HenriqueCCdA/onidata-api/actions/workflows/CI.yml)

 A documentação da `api` fica disponível em `/docs/`. As libs utilizadas

| libs              | descrição                                          |
| ----------------- | -------------------------------------------------- |
| django            | Framework web                                      |
| restframework     | Extenão para contrução de APIs para o django       |
| psycopg           | Driver para postgres                               |
| drf-spectacular   | Documenação em OpenAPI                             |
| gunicorn          | Servidor de aplicação                              |
| python-decouple   | Variáveis de ambiente                              |
| dj-database-url   | URL de banco de dados Django                       |
| django-extensions | Funcionalidades extra para manege.py               |
| pytest            | Framework de teste                                 |
| coverage          | Cobertura de teste                                 |
| ruff              | Formatador / Linter                                |
| black             | Formatador                                         |
| taskipy           | Tarefas                                            |
| faker             | Geradores de dados Fake para testes                |
| model-bakery      | Gerador de dados do Modelos do Djanfo para testes  |

## Simulando o ambiente de produção

Para simular o ambiente de produção simplificado foi usado o `nginx` como `proxy reverso` escutando na porta `80`. Os serviços do `app` e do banco de dados estão isolados dentro da rede do `docker`. A imagem da `app` é definida no `Dockerfile.prod` e a orquestração dos `containers` no `docker-compose-prod.yml`. Os arquivos
estáticos do `admin` foram servidos pelo `nginx`. A coleta dos arquivos estáticos é feita no `docker-compose-prod.yml`.

Para subir os containers basta:

```bash
docker compose -f docker-compose-prod.yml up -d
```

A documentação estará disponivel [http://localhost/docs/](http://localhost/docs/).

## Pré-commit

Para habilitar o pre commit basta:

```bash
pre-commit install
```

## Subindo o banco de dados

Para o banco de dados foi usado a imagem `postgres:16.1-alpine`.

Subindo o banco de dados com `taskipy`:

```bash
task up_db
```

Ou pode-se subir direto com o `docker compose`:

```bash
docker compose -f docker-compose-dev.yml up database -d
```

## Desenvolvimento local

Para instalar as dependencias:

```bash
poetry install --no-root
```

Subindo o servidor:

```bash
python manage.py runserver
```

A documentação estará disponivel [http://localhost:8000/docs/](http://localhost:8000/docs/).


Rodando os testes:

```bash
pytest
```

Foi usado o pacote `pytest-randomly` então a ordem dos teste é aleatoria. Para rodar os teste sempre na mesma ordem:

```bash
pytest -p no:randomly
```

Formatar o código com `black` e `ruff`:

```bash
task fmt
```

Para usar o `ruff` como linter:

```bash
task linter
```

Para subir o servidor local com `gunicorn`

```bash
task server_prod
```

## Desenvolvimento com Docker

Caso você queria é possivel desenvolver interiamente em `conteiners`. A imagem da `app` é definida em `Dockerfile.dev` e a orquestração dos `containers` em `docker-compose-dev.yml`.

Para subir os `conteiners` da aplicação e banco de dados:

```bash
docker compose -f docker-compose-dev.yml up -d
```

A documentação estará disponivel [http://localhost:8000/docs/](http://localhost:8000/docs/).

Para rodar os testes.

```bash
docker compose -f docker-compose-dev.yml run api pytest
```

Para ver os logs

```bash
docker compose -f docker-compose-dev.yml logs
```

Caso você queria acompanhar o log de um serviço específico:

```bash
docker compose -f docker-compose-dev.yml logs api -f
```

Formatar o código com `black` e `ruff`:

```bash
docker compose -f docker-compose-dev.yml run api task fmt
```

Para usar o `ruff` como linter:

```bash
docker compose -f docker-compose-dev.yml run api task lint
```
