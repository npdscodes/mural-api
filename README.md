# mural-api
Web Rest API do MURAL:  plataforma de colaboração Aluno-Professor/Aluno 

## Use virtualenv e Python 3.5
```bash
> pip install virtualenv
> which python3
> virtualenv <env_name> -p <python3_interpreter_directory>
> source <env_name>/bin/activate
```

## Instale as dependências 
```bash
> cd mural-api/
> pip install -r requirements.txt
```

## Migrações e arquivo de parametros
```bash
> cp .env_example .env
> python manage.py migrate
```

## Execute
```bash
> python manage.py runserver
```
