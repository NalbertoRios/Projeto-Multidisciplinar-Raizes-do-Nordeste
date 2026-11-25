# Rede Raízes do Nordeste — Backend

API REST desenvolvida como parte do Projeto Multidisciplinar do curso de Análise e Desenvolvimento de Sistemas.

O sistema simula o backend de uma rede de franquias de alimentação, centralizando operações de usuários, unidades, produtos, estoque, pedidos, pagamentos e programa de fidelidade.

## 1. Objetivo do Projeto

Desenvolver uma API REST para gerenciar as operações de uma rede fictícia de franquias, permitindo que diferentes canais de atendimento utilizem uma estrutura centralizada.

A aplicação contempla os canais:

- APP
- TOTEM
- BALCAO
- PICKUP
- WEB

## 2. Tecnologias Utilizadas

| Tecnologia | Finalidade |
|---|---|
| Python 3.12 | Linguagem de programação |
| FastAPI | Desenvolvimento da API REST |
| SQLAlchemy | Mapeamento objeto-relacional (ORM) |
| SQLite | Banco de dados |
| Pydantic | Validação e estruturação de dados |
| Pydantic Settings | Gerenciamento de configurações |
| PyJWT | Autenticação baseada em tokens JWT |
| pwdlib + Argon2 | Hash seguro de senhas |
| Uvicorn | Servidor ASGI |
| Pytest | Testes automatizados |
| HTTPX | Cliente HTTP utilizado no ambiente de testes |

## 3. Funcionalidades Implementadas

- Cadastro e autenticação de usuários.
- Autenticação utilizando tokens JWT.
- Controle de acesso por perfil de usuário.
- Cadastro, consulta, atualização e desativação de produtos.
- Cadastro, consulta, atualização e desativação de unidades.
- Associação de produtos às unidades, com possibilidade de preço específico e disponibilidade.
- Consulta e atualização de estoque.
- Criação de pedidos vinculados a clientes e unidades.
- Simulação de aprovação e recusa de pagamentos.
- Registro e revogação de consentimentos.
- Consulta de saldo e histórico de pontos do programa de fidelidade.

### Regras de negócio relevantes

- O estoque é controlado por unidade e produto.
- A baixa de estoque ocorre após a aprovação do pagamento.
- As tentativas de pagamento são registradas para preservar seu histórico.
- O programa de fidelidade credita 1 ponto por real pago, descartando frações.
- O crédito de pontos depende de pagamento aprovado e adesão ativa ao programa de fidelidade.
- O cliente consulta somente suas próprias informações de fidelidade.

## 4. Arquitetura do Projeto

A aplicação utiliza uma organização em camadas, separando responsabilidades:

- **API:** disponibiliza os endpoints e recebe as requisições HTTP.
- **Application:** concentra serviços e regras de aplicação.
- **Domain:** contém os modelos e enums do domínio.
- **Infrastructure:** concentra recursos de infraestrutura, incluindo a conexão com o banco de dados.
- **Schemas:** define os modelos de entrada e saída utilizados na API.

### Estrutura de diretórios

```text
app/
├── main.py
├── api/
│   ├── routes/
│   └── dependencies.py
├── application/
│   └── services/
├── core/
├── domain/
│   ├── enums/
│   └── models/
├── infrastructure/
│   └── database/
├── schemas/
tests/
```

## 5. Requisitos para Execução

Para executar o projeto, é necessário possuir:

- Python 3.12 ou superior compatível.
- Git (opcional, para clonar o repositório).
- Terminal PowerShell ou equivalente.

## 6. Instalação e Configuração

### 6.1. Obter o projeto

Clone o repositório:

```bash
git clone https://github.com/NalbertoRios/Projeto-Multidisciplinar-Raizes-do-Nordeste.git
cd Projeto-Multidisciplinar-Raizes-do-Nordeste
```

### 6.2. Criar o ambiente virtual

No Windows:

```powershell
python -m venv .venv
```

Ative o ambiente virtual:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 6.3. Instalar as dependências

```powershell
python -m pip install -r requirements.txt
```

## 7. Variáveis de Ambiente

Crie uma cópia do arquivo de exemplo:

```powershell
Copy-Item .env.example .env
```

Configure as variáveis no arquivo `.env`:

```env
APP_NAME=Rede Raizes do Nordeste API
APP_ENV=development

DATABASE_URL=sqlite:///./raizes.db

SECRET_KEY=coloque_uma_chave_segura_aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**Importante:** substitua o valor de `SECRET_KEY` por uma chave aleatória e segura antes de executar o projeto em outro ambiente.

O arquivo `.env` contém configurações locais e não deve ser publicado no repositório. Utilize o `.env.example` como referência.

## 8. Inicialização do Banco de Dados

Com o ambiente virtual ativado e as dependências instaladas, execute:

```powershell
python -m app.infrastructure.database.init_db
```

O comando cria as tabelas do banco de dados SQLite que ainda não existirem.

O banco é configurado por meio da variável `DATABASE_URL`.

## 9. Executar a API

Na raiz do projeto, execute:

```powershell
uvicorn app.main:app --reload
```

Por padrão, a aplicação ficará disponível em:

```text
http://127.0.0.1:8000
```

## 10. Documentação Interativa

O FastAPI disponibiliza a documentação interativa dos endpoints por meio do Swagger UI:

```text
http://127.0.0.1:8000/docs
```

A documentação alternativa pode ser acessada em:

```text
http://127.0.0.1:8000/redoc
```

O arquivo `openapi.json`, quando gerado, contém a especificação OpenAPI da aplicação.

## 11. Autenticação

A API utiliza autenticação baseada em JWT (JSON Web Token).

O fluxo básico consiste em:

1. Realizar o cadastro de usuário.
2. Efetuar login com as credenciais cadastradas.
3. Obter o token JWT.
4. Utilizar o token nas requisições que exigem autenticação.

No Swagger UI, utilize o recurso **Authorize** para informar o token de acesso.

## 12. Executar os Testes

Com o ambiente virtual ativado, execute:

```powershell
python -m pytest -v
```

O projeto possui teste automatizado para verificar a criação das principais tabelas do banco de dados de testes.

### Resultado registrado

Na execução realizada durante o desenvolvimento:

- Testes executados: 1.
- Testes aprovados: 1.
- Testes reprovados: 0.
- Avisos: 1.

O aviso apresentado está relacionado à integração entre Starlette e HTTPX no cliente de testes e não impediu a aprovação do teste.

Além dos testes automatizados, foram realizadas validações funcionais manuais utilizando o Swagger UI.

## 13. Segurança e Proteção de Dados

O projeto contempla mecanismos relacionados à segurança e à proteção de dados pessoais:

- Autenticação com JWT.
- Armazenamento de senhas utilizando hash Argon2.
- Controle de acesso por perfil.
- Separação das informações de clientes e atendentes nos pedidos.
- Registro e revogação de consentimentos.
- Consulta de informações de fidelidade restrita ao próprio cliente.

O tratamento de dados pessoais deve observar os princípios e requisitos aplicáveis da Lei Geral de Proteção de Dados Pessoais (LGPD).

## 14. Escopo e Melhorias Futuras

O projeto foi desenvolvido com foco em um MVP acadêmico.

Entre as possibilidades de evolução estão:

- Ampliação da cobertura de testes automatizados.
- Implementação de migrações de banco de dados.
- Integração com gateway real de pagamentos.
- Implementação de auditoria completa das operações.
- Ampliação dos recursos do programa de fidelidade.
- Implementação de monitoramento e implantação automatizada.

## 15. Considerações Finais

O backend Rede Raízes do Nordeste demonstra a aplicação prática de conceitos de desenvolvimento de APIs REST, arquitetura em camadas, persistência de dados, autenticação, controle de acesso, regras de negócio, testes e proteção de dados.

A solução foi construída utilizando tecnologias do ecossistema Python, com organização modular e documentação interativa para facilitar sua utilização e evolução.