# EducaBot

 - [**Introdução e Objetivos do Projeto**](#intro-to-the-project)
 - [**Instalação / Execução local**](#local-settings)
 - [**Deploy em produção (VPS)**](#vps-settings)
<!---
[WHITESPACE RULES]
- Different topic = "20" Whitespace character.
--->




















---

<div id="intro-to-the-project"></div>

## 🎯 Introdução e Objetivos do Projeto

> Em breve...




















---

<div id="local-settings"></div>

## 🔧 Instalação / Execução local

Para instalar asconfigurações locais do projeto, vamos utilizar o script `init_project.sh` que executa vários comandos para configurar o projeto:

```bash
make init_project
```

Esse script vai seguir o seguinte fluxo:

```bash
Carrega .env
    ↓
Sobe Docker
    ↓
Aguarda PostgreSQL
    ↓
Atualiza sistema
    ↓
Instala Python
    ↓
Cria .venv
    ↓
Instala dependências
    ↓
Executa migrations
    ↓
Insere gestores
    ↓
Projeto pronto
```




















---

<div id="vps-settings"></div>

## 🚀 Deploy em produção (VPS)

> **⚠️ NOTE:**  
> É comum ao abrir uma VPS ela já vir como `root` por padrão. Então, todos os comandos abaixo já vem do *pressuposto* que serão executados como `root`.

### `Atualizando os pacotes`

Assim que entrar na VPS atualize os pacotes do sistema:

```bash
apt-get update
```

```bash
apt-get upgrade
```

### `Instalando o Docker`

> Agora, vamos instalar o Docker.

Vamos começar removendo os resquícios instalados do Docker (se tiver):

```bash
apt remove docker docker-engine docker.io containerd runc
```

Agora, vamos instalar as dependências:

```bash
apt install ca-certificates curl gnupg lsb-release -y
```

Continuando, agora vamos cria a pasta `/etc/apt/keyrings` com permissões seguras para guardar chaves GPG de repositórios:

```bash
mkdir -m 0755 -p /etc/apt/keyrings
```

Agora, vamos baixar a chave GPG oficial do Docker e a converte para o formato binário aceito pelo APT, salvando no diretório de chaves do sistema:

```bash
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
```

Agora, precisamos Adicionar repositório do Docker:

```bash
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

Vamos atualizar os pacotes novamente:

```bash
apt update && sudo apt upgrade -y
```

Ótimo, agora sim vamos instalar o Docker e Compose:

```bash
apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y
```

**⚠️ NOTE:**  
O Docker, por padrão, só permite que o root (ou membros do grupo docker) executem comandos. Criar o grupo docker permite conceder permissão a usuários comuns sem precisar usar sudo o tempo todo:

```bash
groupadd docker
```

Isso coloca o usuário atual no grupo docker, permitindo executar comandos como `docker ps`:

```bash
usermod -aG docker $USER
```

> **AGORA REINICIE O TERMINAL.**

### `Clonando o repositório`

Aqui, vamos começar clonando o repositório e baixando as dependências:

```bash
git clone https://github.com/rodrigols89/educabot
```

```bash
cd educabot
```

### `Adicionando as variáveis de ambiente`

Outro passo importante vai ser adicionar as variáveis de ambiente:

```bash
nano .env
```

Adicione as variáveis de ambiente:

**.env**
```bash
# ==========================
# POSTGRESQL
# ==========================
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# ==========================
# DATABASE URL (FastAPI)
# ==========================
# dialect+driver://username:password@host:port/database
DATABASE_URL=

# ==========================
# EVOLUTION API
# ==========================
EVOLUTION_API_URL=http://localhost:8080
EVOLUTION_INSTANCE=
EVOLUTION_API_KEY=
```

Aperte `CTRL + x`, `y` e depois `ENTER` para salvar.

```bash
nano .env.evolution
```

**.env.evolution**
```bash
# ==========================
# EVOLUTION API
# ==========================
AUTHENTICATION_API_KEY=
```

Aperte `CTRL + x`, `y` e depois `ENTER` para salvar.

### `Rodando o script de inicialização do projeto: init_project.sh`

Agora, nós vamos rodar o script de inicialização que executa vários comandos para configurar o projeto:

```bash
make init_project
```

Esses comandos seguem o seguinte fluxo:

```bash
Carrega .env
    ↓
Sobe Docker
    ↓
Aguarda PostgreSQL
    ↓
Atualiza sistema
    ↓
Instala Python
    ↓
Cria .venv
    ↓
Instala dependências
    ↓
Executa migrations
    ↓
Insere gestores
    ↓
Projeto pronto
```

### `Configurando o systemd`

Para configurar um serviço que rode o nosso projeto em background, vamos executar um script que vai fazer todo esse processo automaticamente:

```bash
make init_service
```

 - `systemctl status rag.service`
   - Verificar status.
   - **NOTE:** Esse comando é útil para ver se o serviço iniciou corretamente.
 - `journalctl -u rag.service -f`
   - Ver logs do serviço.
 - `systemctl stop rag.service`
   - Parar o serviço.
 - `systemctl restart rag.service`
   - Reiniciar o serviço.

---

**Rodrigo** **L**eite da **S**ilva - **rodirgols89**
