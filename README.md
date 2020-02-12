# Teste de exportação de planilha XLS utilizando Django 3 e DjangoRestFramework

## Instalação

### 1 - Crie o ambiente virtual
```bash
python3 -m venv meuambiente
```

### 2 - Ative seu ambiente virtual
```bash
source meuambiente/bin/activate
```
digite ```deactivate``` para desativar o ambiente da sua sessão

### 3 - Instale suas dependencias
```bash
pip install -r requirements.txt
```

### 4 - Crie as tabelas: Gere as migrações e depois aplique no banco
```bash
./manage.py makemigrations
./manage.py migrate
```

### 5 - Inicie a aplicação
```bash
./manage.py runserver
```


- Para popular com 5000 registros basta acessar ```localhost:8000/api/populate/```
- Listagem de usuarios ```localhost:8000/api/download/``` (para exportar xls basta alterar o formato ou passar o parâmetro ```?format=xls```)
