# `📁 alembic/`

> A pasta `alembic/` é responsável pelo controle de versões do banco de dados.

 - Ela armazena as migrations, que são arquivos que registram as alterações realizadas na estrutura das tabelas ao longo do tempo. 
 - Com o Alembic, é possível criar, aplicar e reverter mudanças no banco de forma organizada e versionada, mantendo o *schema* sincronizado com os modelos *SQLAlchemy* da aplicação.

## Conteúdo

 - [`versions/`](#versions-folder)
 - [`env.py`](#env-py)
 - [`script.py.mako`](#script-py-mako)
<!---
[WHITESPACE RULES]
- "20" Whitespace character.
--->




















---

</div id="versions-folder"></div>

## `versions/`

> A pasta `versions/` contém todas as migrations geradas pelo Alembic.

 - Cada arquivo dessa pasta representa uma alteração específica na estrutura do banco de dados, como:
   - Criação de tabelas;
   - Inclusão de colunas;
   - Ou modificação de índices.
 - O Alembic utiliza esses arquivos para atualizar ou reverter o schema do banco de forma controlada e versionada.




















---

<div id="env-py"></div>

## `env.py`

> O arquivo `env.py` é o principal arquivo de configuração do Alembic.

 - Ele é responsável por conectar o Alembic ao banco de dados e aos modelos *SQLAlchemy* da aplicação, permitindo que as migrations sejam geradas e executadas corretamente.
 - Sempre que comandos como `alembic revision` ou `alembic upgrade` são executados, o `env.py` é carregado para preparar o ambiente de migração.




















---

<div id="script-py-mako"></div>

## `script.py.mako`

> O arquivo `script.py.mako` é um template utilizado pelo *Alembic* para gerar novos arquivos de migration.

 - Sempre que o comando `alembic revision` é executado, o Alembic usa esse modelo como base para criar a estrutura padrão da migration, incluindo informações como:
   - Identificador da revisão;
   - Dependências
   - Funções `upgrade()` e `downgrade()`.

> **NOTE:**  
> Normalmente esse arquivo raramente precisa ser alterado.

---

**Rodrigo** **L**eite da **S**ilva - **rodrigols89**
