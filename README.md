# Rede-Social-de-Sobrevivencia-Zumbi

Este projeto foi feito com:

- Python 3.8
- Django 3.1.4
- Django REST Framework 3.12.2
- PostgreSQL 13
- Docker
- Docker Compose

# Pontos de Extremidade da API REST:

1. `url/api/cadastrar/`: detalhes em 

2. `url/api/login/`: detalhes em 

3. `url/api/sobrevivente/`: detalhes em 

4. `url/api/relatarInfectado/`: detalhes em 

5. `url/api/item/`: detalhes em 

6. `url/api/recursos/trocar/`: detalhes em 

7. `url/api/relatorios/infectados/`: detalhes em 

8. `url/api/relatorios/NaoInfectados/`: detalhes em 

9. `url/api/relatorios/recurso/sobrevivente/`: detalhes em 

10. `url/api/relatorios/pontosPerdidos/`: detalhes em 

## Configurações de Uso

Você irá precisar copiar o arquivo que está na raiz do projeto chamado `.env.sample` para um arquivo chamado `.env`

```sh
cp .env.sample .env
```

O arquivo `.env` deve conter as credenciais do projeto. Para gerar a `SECRET_KEY`, execute em seu terminal o seguinte comando:

```sh
python -c "import secrets; print(secrets.token_urlsafe())"
```

O resultado deste comando deve ser inserido no arquivo `.env` na variável `SECRET_KEY`.

### Configurações Locais

Com todas as dependências instaladas e os comandos anteriores concluídos, você deve seguir esses passos:

1. Criar uma virtualenv na sua máquina. Aqui está um tutorial ótimo de como fazer isso: [tutorial](https://tutorial.djangogirls.org/en/installation/#virtualenv)

2. Instale os pacotes:

```sh
pip install -r requirements-dev.txt
```

3. Depois de instalar todos os pacotes do `requirements-dev.txt`, execute os seguintes comandos:

```sh
python manage.py makemigrations
python manage.py migrate
```

4. Por fim, inicie o servidor de desenvolvimento do Django:

```sh
python manage.py runserver 0.0.0.0:8000
```

### Configurações do Docker

A configuração mais curta, basta executar o comando `docker-compose up` ou `sudo docker-compose up` caso o seu computador exiga permissões.

### Usando o Docker

  * Para ler o arquivo Dockerfile novamente: use o comando `docker-compose up --build`
  
  * Executar o docker em segundo plano: use o comando `docker-compose up -d`
  
  * Para interromper um contêiner: user o comando `docker-compose down`
  
  * Para executar um comando python/Django usando o Docker: use `docker-compose exec web <<O comando que você quer>>`
 
Exemplo:
   
   `docker-compose exec web python manage.py createsuperuser`

### Testes

Para rodar os testes, use os comandos:

`docker-compose up -d`

&&

`docker-compose exec web python manage.py test`
