# Rede-Social-de-Sobrevivencia-Zumbi

## URL DA APLICAÇÃO

```sh
https://zssn-teste.herokuapp.com/
```

Pode levar um tempo maior pra carregar, pois a API está hospedada em um plano Gratuito. Para acessar o Portal do ADMIN, as credenciais são => **username**: admin e **senha**: admin

## Quadro KANBAN utilizado no Desenvolvimento do Projeto

* [QUADRO](https://github.com/ianAraujj/Rede-Social-de-Sobreviv-ncia-Zumbi/projects/1)


## Este projeto foi feito com:

- Python 3.8
- Django 3.1.4
- Django REST Framework 3.12.2
- Django REST Framework-JWT 1.11.0
- PostgreSQL 13
- Docker
- Docker Compose

# Pontos de Extremidade da API REST:

1. `url/api/cadastrar/`: detalhes em [Cadastro de Sobrevivente](https://github.com/ianAraujj/Rede-Social-de-Sobreviv-ncia-Zumbi/wiki/Cadastrar-Sobrevivente)

2. `url/api/login/`: detalhes em [LOGIN](https://github.com/ianAraujj/Rede-Social-de-Sobreviv-ncia-Zumbi/wiki/LOGIN)

3. `url/api/sobrevivente/`: detalhes em [Sobrevivente](https://github.com/ianAraujj/Rede-Social-de-Sobreviv-ncia-Zumbi/wiki/Sobrevivente)

4. `url/api/relatarInfectado/`: detalhes em [Relatar Infectado](https://github.com/ianAraujj/Rede-Social-de-Sobreviv-ncia-Zumbi/wiki/Relatar-Infectado)

5. `url/api/item/`: detalhes em [Item](https://github.com/ianAraujj/Rede-Social-de-Sobreviv-ncia-Zumbi/wiki/Item)

6. `url/api/recursos/trocar/`: detalhes em [Trocar Itens](https://github.com/ianAraujj/Rede-Social-de-Sobreviv-ncia-Zumbi/wiki/Trocar-Itens)

7. `url/api/relatorios/infectados/`: detalhes em [Infectados](https://github.com/ianAraujj/Rede-Social-de-Sobreviv-ncia-Zumbi/wiki/Relat%C3%B3rio-Infectados)

8. `url/api/relatorios/NaoInfectados/`: detalhes em [Nao Infectados](https://github.com/ianAraujj/Rede-Social-de-Sobreviv-ncia-Zumbi/wiki/Relat%C3%B3rio-Sobreviventes-N%C3%A3o-Infectados)

9. `url/api/relatorios/recurso/sobrevivente/`: detalhes em [Media de Recursos](https://github.com/ianAraujj/Rede-Social-de-Sobreviv-ncia-Zumbi/wiki/Relat%C3%B3rio-Recurso-Por-Sobrevivente)

10. `url/api/relatorios/pontosPerdidos/`: detalhes em [Pontos Perdidos](https://github.com/ianAraujj/Rede-Social-de-Sobreviv-ncia-Zumbi/wiki/Pontos-Perdidos)

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

1. Criar uma virtualenv na sua máquina. Aqui está um tutorial ótimo de como fazer isso: [Tutorial Django Girls](https://tutorial.djangogirls.org/en/installation/#virtualenv)

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
