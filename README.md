
# APP LIGA MAXIMUS

Este é um esboço preliminar do README para o projeto "APP LIGA MAXIMUS", que está atualmente nas fases iniciais de desenvolvimento.

## Visão Geral

"APP LIGA MAXIMUS" é um aplicativo projetado para gerenciar e acompanhar informações de ligas de premiação corporativa, com foco em fornecer atualizações de rankings em tempo real e outras métricas relevantes. O projeto ainda está na fase conceitual, e o objetivo principal é criar uma interface amigável que permita o registro de equipes, consulta de rankings e acompanhamento de pontuações.

## Funcionalidades (Planejadas)

- **Cadastro de Equipes**: Permitir que os usuários registrem novas equipes com detalhes como nome e tipo da equipe.
- **Rankings**: Exibir um ranking em tempo real com base no desempenho das equipes.
- **Acompanhamento de Pontuações**: Acompanhar pontos e outras métricas para diferentes categorias (por exemplo, VGV, plantão).
- **Visualização de Dados**: Fornecer interfaces intuitivas para navegar pelas equipes e suas pontuações.

## Tecnologia Utilizada

### Front-End
- **Linguagens**: HTML, JavaScript e Tailwind
- **Manipulação de Dados**: Fetch API
- **Interfaces Principais**:
  - Cadastro de Equipes
  - Consulta de Rankings
  - Visualização de Pontos em Tempo Real

### Back-End
- **Linguagem**: Python
- **Framework**: Flask
- **API**: Rotas RESTful para conectar com o front-end

### Banco de Dados
- **Tipo**: SQLite3
- **Estrutura do Banco**:
  - **Equipes**: `ID`, `Nome`, `Tipo da Equipe`
  - **Rankings**: `ID`, `equipe_id`, `Tipo de Ranking`, `Pontuação Total`
  - **Pontuações**: `ID`, `Tipo` (por exemplo, VGV, plantão), `Valor`, `equipe_id`, `Data`

## Como Executar (A ser atualizado)
### Requisitos

Antes de executar o projeto, você precisará instalar as seguintes dependências:

- **Python 3.7** ou superior
- **pip** (gerenciador de pacotes Python)
- **virtualenv** (opcional, mas recomendado)

Além disso, será necessário um banco de dados SQLite ou outro banco de dados relacional, configurado via variável de ambiente `DATABASE_URL`.

### Passo 1: Clonar o Repositório

Clone este repositório para sua máquina local:

```bash
git clone https://github.com/PedrooHAraujoo/Liga_Backend.git
```
### Passo 2: Configurar o Ambiente Virtual

Crie um ambiente virtual para instalar as dependências do projeto:
```bash
cd Liga_Backend
python -m venv venv
```
Ative o ambiente virtual:

## Windows:
```bash
venv\Scripts\activate
```
## Linux/Mac:
```bash
source venv/bin/activate
```
### Passo 3: Instalar as Dependências

Instale as dependências necessárias, listadas no arquivo requirements.txt:
```bash
pip install -r requirements.txt
```
### Passo 4: Configurar Variáveis de Ambiente

Crie um arquivo .env na raiz do projeto e adicione as seguintes variáveis de ambiente:
```bash
SECRET_KEY=seu_segredo_aqui
UPLOAD_FOLDER=seu_caminho_de_upload_aqui
DATABASE_URL=sqlite:///path_to_your_database.db
```
- SECRET_KEY: A chave secreta usada para gerar tokens JWT
- UPLOAD_FOLDER: O diretório onde as imagens de perfil serão salvas
- DATABASE_URL: A URL de conexão com o banco de dados. Se estiver usando SQLite, pode ser algo como sqlite:///app.db. Caso use outro banco de dados, como PostgreSQL ou MySQL, a URL seria algo como:
  - PostgreSQL: postgresql://usuario:senha@localhost:5432/nome_do_banco
  - MySQL: mysql://usuario:senha@localhost/nome_do_banco

Caso necessário, pode configurar o DEBUG e o FLASK_APP:
```bash
DEBUG=True
FLASK_APP=app.py
```
## Passo 5: Inicializar o Banco de Dados

O projeto utiliza SQLite por padrão, mas a URL de conexão com o banco de dados pode ser configurada via a variável DATABASE_URL. Quando a aplicação for executada pela primeira vez, o banco de dados será criado automaticamente com base no modelo.

Se preferir criar o banco manualmente ou utilizar outro banco de dados, basta configurar a URL de conexão no .env.

Caso precise inicializar o banco de dados antes de rodar o servidor pela primeira vez, você pode usar o seguinte comando no Python:
```bash
from app import db
db.create_all()
```
## Passo 6: Executar o Projeto:

Para iniciar o servidor Flask, execute o seguinte comando:
```bash
python app.py
```
O servidor será iniciado na porta 5000 por padrão. Você pode acessar a aplicação através de:
```bash
http://127.0.0.1:5000
```

As instruções para configurar o projeto localmente serão fornecidas conforme o desenvolvimento avança.

## Status do Projeto

Este projeto ainda está na fase de desenvolvimento. Algumas funcionalidades e tecnologias podem mudar à medida que o projeto evolui.

---

Caso precise de mais atualizações ou modificações, estou à disposição!
