# Projeto Multidisciplinar Backend - Rede Raízes do Nordeste

## Arquitetura e Organização em Camadas

Para atender aos padrões de qualidade, manutenibilidade e separação de responsabilidades exigidos pelo roteiro da trilha Back-End da UNINTER, o projeto da **Rede "Raízes do Nordeste"** foi estruturado em uma arquitetura limpa dividida em quatro camadas principais.

---

## Parte 1 – Arquitetura Aplicada ao Projeto

### 1. Camada de API / Interface (`/api` ou `/controllers`)
- **Responsabilidade:** Porta de entrada da aplicação. Define endpoints HTTP, contratos de entrada (*request*) e saída (*response*), aplica autenticação JWT e gera documentação automática via Swagger/OpenAPI.
- **Ferramenta:** FastAPI com suporte nativo a OpenAPI.
- **Exemplos no projeto:**
  - `POST /auth/login` → autenticação de usuários.
  - `POST /pedidos` → criação de pedidos com canal de origem.
  - `GET /unidades/{id}/cardapio` → consulta de cardápio filtrado por unidade.

### 2. Camada de Aplicação / Casos de Uso (`/application` ou `/services`)
- **Responsabilidade:** Orquestra os fluxos de negócio. Recebe dados validados da API, aplica regras, interage com o domínio e infraestrutura, e retorna o resultado.
- **Ferramenta:** Serviços Python organizados em classes/funções.
- **Exemplos no projeto:**
  - `PedidoService` → valida itens, calcula total, chama mock de pagamento e atualiza estoque.
  - `EstoqueService` → garante consistência de estoque em horários de pico usando transações.
  - `FidelizacaoService` → gerencia pontos de clientes e consentimento LGPD.

### 3. Camada de Domínio (`/domain` ou `/models`)
- **Responsabilidade:** Coração do negócio. Contém entidades e regras invariáveis, independentes de frameworks.
- **Ferramenta:** Pydantic models para tipagem e validação.
- **Entidades previstas:**
  - `Pedido` → exige `canalPedido` válido e fluxo de status controlado.
  - `Produto` → contém preço, estoque e vínculo com unidade.
  - `Cliente` → registra consentimento e pontos de fidelização.
  - `Unidade` → representa cada franquia com estoque próprio.
- **Regras aplicadas:**
  - Pedido só pode ser confirmado se houver estoque suficiente.
  - Cancelamento só pode ocorrer antes do status `PRONTO`.
  - Fidelização só é aplicada com consentimento explícito.

### 4. Camada de Infraestrutura (`/infrastructure` ou `/repositories`)
- **Responsabilidade:** Comunicação com banco de dados e serviços externos.
- **Ferramenta:** SQLAlchemy + SQLite para persistência; mock de pagamento para integração simulada.
- **Exemplos no projeto:**
  - Repositórios para `PedidoRepository`, `ProdutoRepository`, `ClienteRepository`.
  - Configuração do banco relacional e migrações.
  - Implementação da API externa simulada de pagamento (*mock*).
- **Visão futura:** Substituição do SQLite por PostgreSQL em produção e integração com serviços reais de pagamento.

### Fluxo Geral da Arquitetura
1. **API** recebe requisição do cliente (ex.: criação de pedido).  
2. **Aplicação** orquestra o caso de uso (valida itens, chama pagamento).  
3. **Domínio** aplica regras de negócio (estoque, canalPedido, fidelização).  
4. **Infraestrutura** persiste dados e integra serviços externos (mock de pagamento).  
5. Resposta retorna pela **API** ao cliente.

---

## Parte 2 – Fundamentos Teóricos (Didática)

### Camada de API / Interface
- **Função geral:** Porta de entrada da aplicação, responsável por receber requisições externas e devolver respostas.
- **Conceito:** Define contratos de comunicação (inputs/outputs), aplica autenticação e expõe serviços.
- **Independente de tecnologia:** Pode ser uma API REST, GraphQL, gRPC ou até interface de linha de comando.

### Camada de Aplicação / Casos de Uso
- **Função geral:** Orquestra o fluxo de execução das regras de negócio.
- **Conceito:** Coordena interações entre API, domínio e infraestrutura.
- **Independente de tecnologia:** Pode ser implementada em qualquer linguagem, desde que mantenha a lógica de coordenação.

### Camada de Domínio
- **Função geral:** Coração do negócio, contendo entidades e regras invariáveis.
- **Conceito:** Deve ser independente de frameworks, bancos ou detalhes técnicos.
- **Independente de tecnologia:** Representa as regras que não mudam, seja em Python, Java ou qualquer outra linguagem.

### Camada de Infraestrutura
- **Função geral:** Lida com persistência e integrações externas.
- **Conceito:** Implementa detalhes técnicos (banco de dados, APIs externas, filas de mensagens).
- **Independente de tecnologia:** Pode usar SQL, NoSQL, arquivos, serviços externos — mas sempre isolado do domínio.
