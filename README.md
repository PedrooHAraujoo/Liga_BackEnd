
# APP LIGA COHAB

Este é um esboço preliminar do README para o projeto "APP LIGA COHAB", que está atualmente nas fases iniciais de desenvolvimento.

## Visão Geral

"APP LIGA COHAB" é um aplicativo projetado para gerenciar e acompanhar informações de ligas de premiação coorporativa, com foco em fornecer atualizações de rankings em tempo real e outras métricas relevantes. O projeto ainda está na fase conceitual, e o objetivo principal é criar uma interface amigável que permita o registro de equipes, consulta de rankings e acompanhamento de pontuações.

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

As instruções para configurar o projeto localmente serão fornecidas conforme o desenvolvimento avança.

## Status do Projeto

Este projeto ainda está nas fases iniciais de planejamento e desenvolvimento. Algumas funcionalidades e tecnologias podem mudar à medida que o projeto evolui.
