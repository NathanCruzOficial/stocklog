# StockLog — Arquitetura do Projeto

**Versão:** 21.0  
**Arquitetura:** Monorepo — Frontend + Backend  
**Ambiente principal:** Windows  
**Banco de dados:** PostgreSQL  
**Backend:** Python + FastAPI  
**Frontend:** React + JavaScript + Vite + Tailwind CSS

---

# 1. Visão geral

O StockLog será desenvolvido em um único repositório, com separação entre as responsabilidades de frontend, backend, infraestrutura e distribuição.

A arquitetura terá dois componentes principais:

- **StockLog Server:** aplicação central responsável pela API, interface web, banco de dados, autenticação, regras de negócio e integrações.
- **StockLog Client:** inicialmente será o navegador do operador, que acessará o endereço local do servidor. Posteriormente, poderá existir uma aplicação desktop baseada em PyWebView.

## 1.1. Funcionamento

### Cliente

O operador poderá acessar o sistema de duas maneiras:

1. Navegador: acessa o endereço local do servidor e executa a interface React.
2. Aplicação desktop: futuramente, uma janela PyWebView carregará a mesma interface React através da URL do servidor.

### Servidor

O computador central executará:

- React compilado, disponibilizado pelo FastAPI.
- FastAPI, responsável pelas operações e regras de negócio.
- PostgreSQL, responsável pela persistência dos dados.
- Workers, responsáveis pelas tarefas em segundo plano e sincronizações.

O servidor ficará responsável por centralizar todas as operações do estabelecimento.

---

# 2. Estrutura principal do projeto

```text
StockLog/
│
├── backend/                         # Backend e lógica do servidor
│   ├── app/
│   │   ├── api/                     # Rotas e endpoints da API
│   │   │   └── v1/                  # Primeira versão da API
│   │   │
│   │   ├── core/                    # Configurações e componentes centrais
│   │   │   ├── config.py            # Configurações e variáveis de ambiente
│   │   │   ├── security.py          # Segurança, hash e tokens
│   │   │   ├── dependencies.py      # Dependências compartilhadas
│   │   │   └── permissions.py       # Verificação de permissões
│   │   │
│   │   ├── db/                      # Conexão e gerenciamento do banco
│   │   │   ├── session.py           # Sessões SQLAlchemy
│   │   │   └── base.py              # Registro da Base declarativa
│   │   │
│   │   ├── models/                  # Modelos das tabelas
│   │   ├── schemas/                 # Schemas Pydantic
│   │   ├── repositories/            # Consultas e persistência
│   │   ├── services/                # Regras de negócio
│   │   │
│   │   ├── integrations/            # Integrações externas
│   │   │   └── mercadolivre/        # Integração com Mercado Livre
│   │   │
│   │   ├── workers/                 # Tarefas em segundo plano
│   │   │   ├── sync/                # Sincronizações externas
│   │   │   └── outbox/              # Processamento da Transactional Outbox
│   │   │
│   │   ├── utils/                   # Funções auxiliares
│   │   └── main.py                  # Inicialização do FastAPI
│   │
│   ├── migrations/                  # Migrações do Alembic
│   ├── tests/                       # Testes automatizados do backend
│   │   ├── unit/                    # Testes unitários
│   │   ├── integration/             # Testes de integração
│   │   └── conftest.py              # Fixtures compartilhadas
│   │
│   ├── alembic.ini                  # Configuração do Alembic
│   ├── pyproject.toml               # Dependências e configurações Python
│   └── .env.example                 # Exemplo de variáveis do backend
│
├── frontend/                        # Frontend React
│   ├── src/
│   │   ├── assets/                  # Imagens, ícones e recursos visuais
│   │   ├── components/              # Componentes reutilizáveis
│   │   ├── features/                # Funcionalidades organizadas por domínio
│   │   │   ├── auth/                # Autenticação
│   │   │   ├── users/               # Usuários e permissões
│   │   │   ├── products/            # Produtos
│   │   │   ├── inventory/           # Estoque e movimentações
│   │   │   ├── sales/               # Vendas e reservas
│   │   │   ├── integrations/        # Integrações
│   │   │   └── admin/               # Administração do sistema
│   │   │
│   │   ├── layouts/                 # Estruturas visuais compartilhadas
│   │   ├── hooks/                   # Hooks personalizados
│   │   ├── contexts/                # Estados e contextos globais
│   │   ├── services/                # Comunicação com o backend
│   │   ├── lib/                     # Bibliotecas e configurações auxiliares
│   │   ├── utils/                   # Funções auxiliares
│   │   ├── styles/                  # Estilos globais
│   │   ├── App.jsx                  # Componente principal
│   │   └── main.jsx                 # Ponto de entrada do React
│   │
│   ├── public/                      # Arquivos públicos estáticos
│   ├── tests/                       # Testes do frontend
│   ├── package.json                 # Dependências e scripts Node
│   ├── vite.config.js               # Configuração do Vite
│   └── index.html                   # Documento HTML principal
│
├── desktop/                         # Cliente desktop futuro
│   ├── src/
│   │   ├── app.py                   # Inicialização do PyWebView
│   │   └── config.py                # Configurações do cliente desktop
│   │
│   └── resources/                   # Ícones e recursos da aplicação
│
├── deploy/                          # Infraestrutura e distribuição
│   ├── docker/                      # Ambiente de desenvolvimento
│   │   ├── compose.yaml             # Serviços Docker
│   │   └── postgres/                # Configurações auxiliares do PostgreSQL
│   │
│   ├── windows/                     # Preparação do ambiente Windows
│   │   ├── scripts/                 # Scripts de instalação e manutenção
│   │   ├── services/                # Configuração de serviços Windows
│   │   └── config/                  # Modelos de configuração
│   │
│   ├── pyinstaller/                 # Configurações de empacotamento Python
│   │   └── stocklog-server.spec
│   │
│   ├── inno-setup/                  # Instaladores do Windows
│   │   └── stocklog.iss
│   │
│   └── updater/                     # Atualizador futuro
│       ├── app/                     # Lógica do atualizador
│       └── config/                  # Configurações de atualização
│
├── scripts/                         # Scripts de desenvolvimento e automação
│   ├── dev/                         # Inicialização do ambiente de desenvolvimento
│   ├── build/                       # Compilação e preparação de builds
│   └── maintenance/                 # Manutenção e verificações
│
├── docs/                            # Documentação
│   ├── architecture/                # Decisões arquiteturais
│   ├── database/                    # Documentação do banco
│   ├── api/                         # Documentação da API
│   ├── deployment/                  # Instalação e distribuição
│   └── guides/                      # Guias de utilização
│
├── .gitignore                       # Arquivos ignorados pelo Git
├── .env.example                     # Exemplo de configuração geral
├── README.md                        # Apresentação do projeto
└── ARQUITETURA.md                   # Documentação da arquitetura
```

---

# 3. Responsabilidade de cada diretório

## 3.1. Backend

Diretório: `backend/`

Responsável pelo funcionamento interno do StockLog.

### `app/api/`

Contém os endpoints que recebem as requisições do frontend.

Exemplos:
- Autenticação.
- Cadastro de produtos.
- Movimentações.
- Vendas.
- Consultas de estoque.
- Administração.

As rotas devem ser organizadas por domínio e versão da API.

### `app/core/`

Contém configurações e componentes fundamentais.

- `config.py`: leitura das configurações do ambiente.
- `security.py`: hash de senhas, tokens e mecanismos de segurança.
- `dependencies.py`: dependências compartilhadas do FastAPI.
- `permissions.py`: regras de autorização.

### `app/db/`

Responsável pela conexão com o PostgreSQL e gerenciamento das sessões SQLAlchemy.

### `app/models/`

Representa as entidades persistidas no banco de dados.

Exemplos:
- User
- Product
- StockBalance
- StockMovement
- Order
- Listing

### `app/schemas/`

Define os formatos dos dados recebidos e enviados pela API, utilizando Pydantic.

### `app/repositories/`

Centraliza operações de consulta e persistência no banco.

### `app/services/`

Contém as regras de negócio.

Exemplos:
- Cadastrar produtos.
- Reservar estoque.
- Confirmar vendas.
- Cancelar reservas.
- Realizar ajustes de inventário.

### `app/integrations/`

Contém os módulos responsáveis por conversar com serviços externos.

Inicialmente, a integração principal será com o Mercado Livre.

### `app/workers/`

Responsável por executar operações que não precisam ocorrer diretamente durante uma requisição do operador.

Exemplos:
- Sincronização de anúncios.
- Processamento de notificações.
- Tentativas de reenvio.
- Processamento da Transactional Outbox.

### `migrations/`

Armazena o histórico de alterações da estrutura do banco através do Alembic.

### `tests/`

Contém os testes automatizados do backend.

Será utilizado Pytest, com pytest-cov para medir a cobertura dos testes.

---

## 3.2. Frontend

Diretório: `frontend/`

Responsável pela interface visual do StockLog.

Tecnologias:
- React
- JavaScript
- Vite
- Tailwind CSS

### `src/components/`

Componentes reutilizáveis, como botões, tabelas, formulários, modais e menus.

### `src/features/`

Organiza funcionalidades por domínio.

Essa organização permite que cada funcionalidade tenha seus próprios componentes, telas, hooks e serviços quando necessário.

Exemplo:

```text
features/
└── products/
    ├── components/
    ├── hooks/
    ├── pages/
    ├── services/
    └── index.js
```

### `src/pages/`

Caso seja necessário, as páginas globais e telas que não pertencem a uma funcionalidade específica poderão ficar aqui. As páginas específicas dos módulos devem preferencialmente ficar dentro de suas respectivas `features/`.

### `src/services/`

Contém a comunicação HTTP com a API.

### `src/contexts/`

Gerencia estados globais compartilhados, como usuário autenticado e permissões carregadas.

### `src/layouts/`

Contém estruturas visuais compartilhadas, como layout principal, menu lateral e cabeçalho.

### `src/lib/`

Configurações e inicializações de bibliotecas externas.

---

## 3.3. Desktop

Diretório: `desktop/`

Será utilizado futuramente para criar uma aplicação desktop com PyWebView.

Sua função será abrir uma janela própria e carregar a interface React disponibilizada pelo servidor.

Não deverá duplicar regras de negócio nem implementar um segundo frontend.

O cliente desktop continuará consumindo o mesmo servidor utilizado pelo navegador.

---

## 3.4. Deploy

Diretório: `deploy/`

Centraliza os arquivos necessários para preparar, instalar, empacotar e distribuir o StockLog.

### `docker/`

Configura o ambiente de desenvolvimento, inicialmente com PostgreSQL.

### `windows/`

Contém scripts e configurações específicos do Windows.

Exemplos:
- Preparação do ambiente.
- Instalação do PostgreSQL.
- Registro de serviços.
- Configuração de inicialização.
- Verificação do ambiente.
- Rotinas de manutenção.

### `pyinstaller/`

Armazena arquivos `.spec` e configurações necessárias para transformar o backend Python em executáveis distribuíveis.

### `inno-setup/`

Contém os scripts `.iss` utilizados pelo Inno Setup para criar o instalador do StockLog.

### `updater/`

Reservado para o atualizador futuro.

Poderá conter:
- Verificação de novas versões.
- Download de atualizações.
- Validação dos arquivos.
- Aplicação de atualizações.
- Recuperação em caso de falha.

O atualizador deverá respeitar a separação entre arquivos da aplicação e dados persistentes.

---

## 3.5. Scripts

Diretório: `scripts/`

Contém scripts auxiliares que não fazem parte diretamente da aplicação.

- `dev/`: iniciar o ambiente de desenvolvimento.
- `build/`: compilar o frontend e preparar os pacotes.
- `maintenance/`: verificações e manutenção.

---

## 3.6. Docs

Diretório: `docs/`

Centraliza a documentação técnica e operacional.

- `architecture/`: decisões e diagramas arquiteturais.
- `database/`: estrutura e relacionamentos do banco.
- `api/`: documentação dos endpoints.
- `deployment/`: procedimentos de instalação e distribuição.
- `guides/`: manuais e orientações.

---

# 4. Configurações e arquivos de ambiente

As configurações devem ficar separadas dos dados persistentes.

| Arquivo | Responsabilidade |
|---|---|
| `.env` | Variáveis privadas do ambiente local |
| `.env.example` | Modelo de variáveis necessárias |
| `backend/app/core/config.py` | Leitura e validação das configurações |
| `backend/pyproject.toml` | Dependências e configurações Python |
| `frontend/package.json` | Dependências e scripts React |
| `frontend/vite.config.js` | Configuração de compilação do frontend |
| `backend/alembic.ini` | Configuração das migrações |
| `deploy/docker/compose.yaml` | Serviços do ambiente Docker |
| `deploy/pyinstaller/` | Configurações de empacotamento |
| `deploy/inno-setup/` | Configurações do instalador |

O `.env` real nunca deverá ser enviado ao Git.

As credenciais de produção devem ficar em diretório protegido, fora do repositório e dos diretórios de instalação.

---

# 5. Paths — Desenvolvimento

O código-fonte e os dados de desenvolvimento serão mantidos separados.

## 5.1. Código-fonte

Exemplo:

```text
D:\Projetos\StockLog\
```

Contém o repositório completo, incluindo backend, frontend, documentação e scripts.

## 5.2. Ambiente Python

```text
D:\Projetos\StockLog\backend\.venv\
```

Ambiente virtual Python utilizado exclusivamente no desenvolvimento.

Não deve ser enviado ao Git nem utilizado como diretório de dados de produção.

## 5.3. Dados locais de desenvolvimento

```text
%LOCALAPPDATA%\StockLog-dev\
├── config/
├── logs/
└── temp/
```

Armazena configurações e arquivos auxiliares específicos do ambiente de desenvolvimento.

## 5.4. Banco de desenvolvimento

O PostgreSQL será executado pelo Docker Compose.

Seus dados serão persistidos em volume Docker, separado do banco de produção.

O volume não deverá ser confundido com os arquivos do repositório.

---

# 6. Paths — Produção

Na instalação de produção, os arquivos executáveis ficarão separados dos dados persistentes.

## 6.1. Arquivos da aplicação

```text
C:\Program Files\StockLog\
│
├── Server\
│   ├── StockLogServer.exe
│   ├── frontend\
│   │   └── dist\
│   └── resources\
│
├── Updater\
│   └── StockLogUpdater.exe
│
└── Desktop\
    └── StockLogClient.exe
```

Responsável por armazenar os executáveis, bibliotecas e arquivos da aplicação.

O diretório `Updater` e o diretório `Desktop` são planejados para versões futuras.

## 6.2. Dados persistentes

```text
C:\ProgramData\StockLog\
│
├── config\
│   └── .env
│
├── database\
│   └── data\
│
├── logs\
│
├── backups\
│
├── updates\
│
└── temp\
```

Responsável por armazenar:

- Configurações de produção.
- Dados do PostgreSQL.
- Logs.
- Backups.
- Arquivos temporários de atualização.
- Arquivos auxiliares de manutenção.

**Importante:** o diretório `database/data` será utilizado como diretório de dados do PostgreSQL instalado no servidor. O PostgreSQL deverá executar como serviço do Windows.

## 6.3. Dados específicos do usuário

```text
%LOCALAPPDATA%\StockLog\
├── config\
└── cache\
```

Reservado para preferências e cache específicos do usuário Windows, caso sejam necessários.

---

# 7. Fluxo de funcionamento

```text
┌────────────────────────────────────────────┐
│              COMPUTADORES CLIENTES          │
│                                            │
│  Navegador                                 │
│      │                                     │
│      └──────> Interface React              │
│                                            │
│  Desktop (futuro)                          │
│      │                                     │
│      └──────> PyWebView                    │
│                                            │
└──────────────────────┬─────────────────────┘
                       │
                       │ Rede local
                       ▼
┌────────────────────────────────────────────┐
│                STOCKLOG SERVER              │
│                                            │
│  ┌──────────────────────────────────────┐  │
│  │             FastAPI                  │  │
│  │                                      │  │
│  │  API + Regras de negócio + Workers   │  │
│  └──────────────┬───────────────────────┘  │
│                 │                          │
│                 ▼                          │
│  ┌──────────────────────────────────────┐  │
│  │             PostgreSQL               │  │
│  └──────────────────────────────────────┘  │
│                                            │
│  React compilado servido pelo FastAPI      │
│                                            │
└──────────────────────┬─────────────────────┘
                       │
                       │ Internet
                       ▼
              Mercado Livre / APIs
```

O navegador recebe os arquivos React do servidor e executa o JavaScript localmente.

Todas as operações de negócio passam pelo FastAPI.

O PostgreSQL não deverá ser acessível diretamente pelos computadores clientes.

---

# 8. Estratégia de atualização

O projeto deverá ser preparado para receber atualizações sem comprometer os dados do estabelecimento.

A atualização deverá diferenciar:

- Arquivos da aplicação.
- Configurações de produção.
- Dados do banco.
- Backups.

Uma atualização não deverá apagar o banco de dados nem sobrescrever configurações personalizadas.

As migrações do Alembic deverão ser executadas de maneira controlada durante as atualizações.

O Updater será desenvolvido posteriormente, depois que o fluxo de instalação e inicialização do servidor estiver estável.

---

# 9. Princípios arquiteturais

1. Monorepo com separação de responsabilidades.
2. Frontend e backend independentes em desenvolvimento.
3. React servido pelo FastAPI em produção.
4. PostgreSQL acessível somente pelo backend.
5. Regras de negócio centralizadas no servidor.
6. Cliente desktop reutilizando a mesma interface React.
7. Configurações separadas dos dados persistentes.
8. Desenvolvimento e produção com diretórios independentes.
9. Integrações externas desacopladas das operações locais.
10. Instalação preparada para distribuição online e futura distribuição offline.
11. Atualizações sem perda de dados.
12. Testes automatizados como parte do desenvolvimento.

---

# 10. Tecnologias previstas

| Área | Tecnologia |
|---|---|
| Backend | Python + FastAPI |
| ORM | SQLAlchemy 2 |
| Banco | PostgreSQL |
| Migrações | Alembic |
| Validação | Pydantic |
| Configurações | Pydantic Settings |
| Autenticação | JWT |
| Testes backend | Pytest |
| Cobertura | pytest-cov |
| Frontend | React |
| Linguagem frontend | JavaScript |
| Build frontend | Vite |
| Estilização | Tailwind CSS |
| Cliente desktop futuro | PyWebView |
| Ambiente de desenvolvimento | Docker Compose |
| Empacotamento Python | PyInstaller |
| Instalador Windows | Inno Setup |
| Controle de versão | Git + GitHub |

---

# 11. Observações

Esta estrutura representa a arquitetura planejada do StockLog, não significa que todos os diretórios e módulos precisam ser criados imediatamente.

Os diretórios deverão ser adicionados conforme as funcionalidades forem implementadas.

A prioridade é construir primeiro uma base funcional, segura e testável. Componentes futuros, como Updater, Desktop e ferramentas de administração, deverão ser integrados sem comprometer a estrutura principal.