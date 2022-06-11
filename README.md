
# MercanTree

Troque ferramentas pagas com recursos desnecessários por um sistema de código aberto com eficiência e minimalismo.



## Funcionalidades


- 📦 Controle de estoque                                                                                                                                                                      
- 💳 Gerenciamento de pagamentos
- 🔔 Alertas do estoque
- 📊 Estatísticas de vendas
- 🕶️ Tema escuro


## Stack utilizada

**Front-end:** Vue, Vite, TailwindCSS, DaisyUI

**Back-end:** Python, Django, Django Rest Framework, SQLite


## Autores

- [@adielCalixto](https://www.github.com/adielCalixto)
- [@Jweinny](https://www.github.com/Jweinny)


## Roadmap

- Aprimorar métodos de pagamento

- Implementar avisos no front-end

- Gerar estatísticas


## Rodando localmente

Clone o projeto

```bash
  git clone https://github.com/adielCalixto/MercanTree
```

Entre no diretório do projeto

```bash
  cd MercanTree
```

### Backend:

Instale as dependências do python

```bash
  pipenv install
```

Execute as migrations

```bash
  pipenv run python manage.py migrate
```

Inicie o servidor

```bash
  pipenv run python manage.py runserver
```

### Frontend:

Entre no diretório do front-end

```bash
  cd mercantree-fe
```

Instale as dependências do node

```bash
  yarn install
```

Inicie o servidor

```bash
  yarn dev
```


