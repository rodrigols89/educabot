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

O **EducaBot** foi desenvolvido para solucionar um processo operacional recorrente na **Secretaria de Educação de Remígio-PB**, onde trabalho:

> A **necessidade de automatizar as solicitações de gás de cozinha e abastecimento de água** realizadas pelas unidades escolares e pela Secretaria de Educação através do WhatsApp.

Antes da implantação do sistema, os responsáveis pelas escolas precisavam entrar em contato manualmente com os fornecedores, gerando retrabalho, dificuldades de controle e ausência de um registro centralizado dos pedidos.

Para resolver esse problema, o EducaBot utiliza a **Evolution API** como gateway de integração com o WhatsApp e uma API desenvolvida em **FastAPI**, responsável por validar solicitações, aplicar regras de negócio, registrar pedidos e encaminhá-los automaticamente ao fornecedor correto.

O sistema transforma mensagens enviadas via WhatsApp em solicitações estruturadas, reduzindo o tempo gasto no processo e garantindo maior padronização, rastreabilidade e confiabilidade das requisições.

### 🎯 Objetivos Técnicos

* Automatizar solicitações de gás e água realizadas via WhatsApp.
* Identificar automaticamente o responsável através do número de telefone.
* Validar comandos enviados pelos usuários autorizados.
* Aplicar regras de negócio antes do processamento dos pedidos.
* Registrar todos os pedidos em banco de dados.
* Evitar pedidos duplicados da mesma categoria no mesmo dia.
* Encaminhar automaticamente cada solicitação ao fornecedor correspondente.
* Permitir configuração do sistema através de variáveis de ambiente.

### 🏗️ Arquitetura do Sistema

A solução é dividida em **quatro camadas principais**:

* **1. Recepção de Eventos (Webhook Layer):**

  * Recebe eventos enviados pela Evolution API.
  * Identifica mensagens recebidas via WhatsApp.
  * Extrai telefone e conteúdo da mensagem.
  * Ignora eventos que não representam comandos válidos.

* **2. Processamento das Regras de Negócio (Business Layer):**

  * Valida os comandos suportados.
  * Localiza o responsável autorizado.
  * Verifica permissões para realização dos pedidos.
  * Impede pedidos duplicados da mesma categoria no mesmo dia.
  * Seleciona automaticamente o fornecedor adequado para cada solicitação.

* **3. Persistência dos Dados (Persistence Layer):**

  * Consulta responsáveis cadastrados.
  * Registra novos pedidos.
  * Consulta pedidos realizados no dia.
  * Mantém o histórico das solicitações em banco PostgreSQL.

* **4. Integração Externa (Notification Layer):**

  * Gera mensagens padronizadas para os fornecedores.
  * Envia solicitações utilizando a Evolution API.
  * Notifica o responsável sobre o resultado da solicitação.
  * Centraliza toda a comunicação realizada pelo sistema via WhatsApp.




















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

Agora, vamos clonar o repositóri para a nossa VPS:

```bash
git clone https://github.com/rodrigols89/educabot
```

```bash
cd educabot
```

### `Adicionando as variáveis de ambiente`

> Outro passo importante vai ser adicionar (atualizar) as variáveis de ambiente.

Aqui você vai ter que modificar o nome do arquivo [.env-example](.env-example) para `.env` e atualizar seus valores.

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

### `Inserindo pessoas (números) autorizados a fazer pedidos`

Agora, que você já aplicou todas as migrações e seu Banco de Dados está disponível é interessante você inserir as pessoas (números) que tem permissões de fazer pedidos:

```bash
source .venv/bin/activate
```

```bash
python insert_responsavel.py
```

**NOTE:**  
> No exemplo acima você vai criar uma cópia do [app/utils/insert_responsavel_example.py](app/utils/insert_responsavel_example.py) e adaptar para seus clientes. Depois e só executar ele na raiz do projeto (igual eu fiz acima).

### `Configurando o Evolution API`

> Agora, nós precisamos aplicar as primeiras configurações do Evolution API.

Comece abrindo o link de acesso do seu serviço:

 - [http://seu-ip:8080/manager](http://seu-ip:8080/manager)

> **NOTE:**  
> Aqui vai se solicitado que você coloque sua `API Key Global`.  
> É a mesma que você definiu em `AUTHENTICATION_API_KEY` nas *variáveis de ambiente (.env)*.

Agora é só você criar uma instância, com:

 - **nome da sua instânica**
 - **Canal**
   - `Baileys`
 - **Token**
   - O mesmo que você definiu em `AUTHENTICATION_API_KEY` nas *variáveis de ambiente (.env)*
 - **Número**
   - Número de telefone que você vai utilizar

Continuando, agora você vai clicar na engrenage:

 - **Configurações**
   - *Comportamento*
     - Ativar -> `Ignorar Grupos`
     - Ativar -> `Sincronizar Histórico Completo`
 - **Eventos**
   - *Webhook*
     - Ativar -> `Ativar ou desativar o webhook (V)`
     - Adicionar URL -> `http://seu-ip:8001/webhook/evolution`
     - Events
       - Ativar -> `MESSAGES_UPSERT`
 - **Salvar!**

Por fim, lembre-se de ler o *QR-Code* para vincular o serviço ao seu *WhatsApp*.

### `Configurando o systemd`

Para configurar um serviço que rode o nosso projeto em background, vamos executar um script que vai fazer todo esse processo automaticamente:

```bash
make init_service
```

 - `systemctl status educabot.service`
   - Verificar status.
   - **NOTE:** Esse comando é útil para ver se o serviço iniciou corretamente.
 - `journalctl -u educabot.service -f`
   - Ver logs do serviço.
 - `systemctl stop educabot.service`
   - Parar o serviço.
 - `systemctl restart educabot.service`
   - Reiniciar o serviço.

---

**Rodrigo** **L**eite da **S**ilva - **rodirgols89**
