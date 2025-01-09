## Funcionalidades

### Autenticação
- **Token JWT (JSON Web Token)**: Implementa autenticação usando JWT para gerenciar sessões de forma mais segura. 
- **Proteção de Rotas**: Adiciona decoradores para proteger rotas que exigem autenticação, permitindo acesso apenas a usuários logados. ###Feito

### Gerenciamento de Perfis
- **Visualização e Edição de Perfil**: Permite a visualização e edição de informações de perfil, como nome, email e Instagram.
- **Upload de Imagem de Perfil**: Adiciona funcionalidade para carregar fotos de perfil.
- **Rota para Servir Arquivos de Upload**: Adiciona a funcionalidade de que os usuários acessem as imagens carregadas.

### Controle de Acesso por Cargos
- **Definição de Cargos e Permissões**: Estrutura de cargos (Admin, Gerente, Corretor, Suporte) com permissões específicas para controlar o que cada usuário pode acessar.
  - **Admin**: Acesso total, incluindo gerenciamento de usuários e logs de atividades.
  - **Gerente**: Acesso a rankings, histórico de pontuações e visualização de informações de equipe.
  - **Corretor**: Acesso à visualização de rankings e pontuações.
  - **Suporte**: Visualização de informações de usuários para auxílio em problemas técnicos.
- **Proteção de Rotas Baseada em Cargos**: Utiliza decoradores para verificar o cargo e permitir ou negar acesso a funcionalidades específicas.
- **Painel de Configuração de Permissões**: Painel onde as permissões podem ser configuradas e ajustadas sem necessidade de modificar o código.

### Funções de Gerenciamento
- **Painel de Administração**: Painel para gerenciar usuários, incluindo a possibilidade de desativar ou excluir contas.
- **Logs de Atividades**: Registro de atividades, como logins, cadastros e alterações no perfil.

### Melhorias de Usabilidade
- **Validação de Formulários**: Validação de dados no frontend para fornecer feedback em tempo real.
- **Mensagens de Erro Mais Detalhadas**: Fornecimento de mensagens de erro mais específicas e úteis.

### Funcionalidades de Ranking
- **Visualização de Rankings**: Endpoints para visualizar rankings de equipes ou pontuações.
- **Histórico de Pontuações**: Visualização do histórico de pontuações e comparações com outros usuários.

### Interação Social
- **Sistema de Comentários**: Implementação de um sistema de comentários sobre pontuações ou conquistas.
- **Notificações**: Sistema de notificações para manter os usuários informados sobre atualizações ou interações.

### Integração com APIs Externas
- **Integração com Redes Sociais**: Login com contas de redes sociais, como Google ou Facebook.
- **Analytics**: Ferramentas de análise para monitorar o uso do aplicativo e identificar áreas de melhoria.

### Testes e Documentação
- **Testes Automatizados**: Testes para rotas e funcionalidades, garantindo que tudo funcione conforme o esperado.
- **Documentação da API**: Documentação usando ferramentas como Swagger ou Postman, facilitando o uso por desenvolvedores.

### Segurança
- **Melhorias de Segurança**: Revisão e melhoria das práticas de segurança, como limitar tentativas de login e implementar verificação em duas etapas (2FA).

### Deploy
- **Hospedagem do Aplicativo**: Consideração para a implantação do aplicativo em plataformas como Heroku, DigitalOcean ou AWS para acessibilidade.

---
