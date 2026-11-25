# Projeto Multidisciplinar Backend - Rede Raízes do Nordeste

## Conformidade com a LGPD e Privacidade

### Tabela de Mapeamento de Dados Pessoais

| Dado Pessoal        | Finalidade                                | Base Legal / Consentimento | Medida de Proteção |
|----------------------|-------------------------------------------|----------------------------|---------------------|
| Nome                 | Identificação do cliente                  | Consentimento explícito     | Armazenamento seguro, acesso restrito |
| E-mail               | Comunicação e login                       | Consentimento explícito     | Hash de credenciais, não expor em responses |
| Telefone             | Contato e notificações de pedidos         | Consentimento explícito     | Uso restrito, não compartilhado com terceiros |
| Histórico de Pedidos | Fidelização e relatórios de consumo       | Consentimento explícito     | Logs de acesso, anonimização após prazo legal |
| Senha                | Autenticação de usuários                  | Execução de contrato        | Hash seguro (bcrypt/Argon2), nunca em texto plano |

### Regras Complementares
- **Minimização de Dados:** O sistema coleta apenas os dados estritamente necessários para a prestação do serviço.  
- **Anonimização e Retenção:** Dados pessoais devem ser anonimizados ou excluídos após o término da relação contratual ou conforme prazo legal.  
- **Logs de Acesso:** Toda consulta ou alteração em dados pessoais deve gerar log com usuário responsável e data/hora.  
- **Direitos do Titular:** O sistema deve possibilitar a exclusão de cadastro e consulta de dados pessoais mediante solicitação do titular.  
- **Proteção de Credenciais:** As senhas dos usuários nunca são armazenadas em texto plano, sendo obrigatório o uso de funções hash criptográficas seguras.  
- **Segurança na Resposta (Response):** Os endpoints da API são projetados para omitir dados confidenciais ou tokens internos nas respostas públicas enviadas aos clientes.  
