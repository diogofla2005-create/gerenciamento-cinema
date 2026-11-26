# Sistema de Gerenciamento de Cinema (Projeto CRUD 2026.2)

Sistema desenvolvido em **Python** integrado ao banco de dados relacional **MySQL** para gestão de Clientes, Filmes e Venda de Ingressos.

## Modelagem e Relacionamentos (DER)

* **Clientes (1) ──── (N) Ingressos:** Um cliente pode comprar vários ingressos; cada ingresso pertence a um único cliente.
* **Filmes (1) ──── (N) Ingressos:** Um filme pode ter vários ingressos vendidos; cada ingresso refere-se a um único filme.

## Dicionário de Dados

### Tabela: `clientes`
| Coluna | Tipo | Restrições | Descrição |
| :--- | :--- | :--- | :--- |
| `id_cliente` | `INT` | `PRIMARY KEY`, `AUTO_INCREMENT` | Identificador único do cliente |
| `nome` | `VARCHAR(100)` | `NOT NULL` | Nome completo do cliente |
| `cpf` | `CHAR(11)` | `NOT NULL`, `UNIQUE` | CPF validado (11 dígitos) |
| `email` | `VARCHAR(120)` | `NOT NULL`, `UNIQUE` | E-mail válido do cliente |
| `telefone` | `VARCHAR(11)` | `NOT NULL` | Telefone com DDD (10 ou 11 dígitos) |
| `data_cadastro` | `TIMESTAMP` | `DEFAULT CURRENT_TIMESTAMP` | Data e hora do cadastro |

### Tabela: `filmes`
| Coluna | Tipo | Restrições | Descrição |
| :--- | :--- | :--- | :--- |
| `id_filme` | `INT` | `PRIMARY KEY`, `AUTO_INCREMENT` | Identificador único do filme |
| `titulo` | `VARCHAR(150)` | `NOT NULL` | Título do filme |
| `genero` | `VARCHAR(50)` | `NOT NULL` | Gênero cinematográfico |
| `duracao_min` | `INT` | `NOT NULL` | Duração em minutos |
| `classificacao` | `VARCHAR(10)` | `NOT NULL` | Classificação indicativa |

### Tabela: `ingressos`
| Coluna | Tipo | Restrições | Descrição |
| :--- | :--- | :--- | :--- |
| `id_ingresso` | `INT` | `PRIMARY KEY`, `AUTO_INCREMENT` | Identificador único do ingresso |
| `id_cliente` | `INT` | `NOT NULL`, `FOREIGN KEY` | Chave estrangeira para `clientes(id_cliente)` (`ON DELETE RESTRICT`) |
| `id_filme` | `INT` | `NOT NULL`, `FOREIGN KEY` | Chave estrangeira para `filmes(id_filme)` (`ON DELETE RESTRICT`) |
| `assento` | `VARCHAR(10)` | `NOT NULL` | Poltrona escolhida |
| `valor` | `DECIMAL(6,2)` | `NOT NULL` | Valor pago pelo ingresso |
| `data_sessao` | `DATETIME` | `NOT NULL` | Data e hora da sessão |

### Restrições de integridade

- As chaves estrangeiras garantem que cada ingresso esteja associado a um cliente e a um filme existentes.
- A restrição `ON DELETE RESTRICT` impede a exclusão de clientes e filmes que possuem ingressos vinculados.
- A restrição `ON UPDATE CASCADE` propaga alterações nas chaves referenciadas.
- A restrição `UNIQUE (id_filme, assento, data_sessao)`, denominada `uq_assento_sessao`, impede a venda duplicada de um mesmo assento para o mesmo filme, na mesma data e horário.

O sistema considera uma sessão por filme em cada data e horário, pois a modelagem atual não possui uma tabela de salas.

## Funcionalidades do Sistema

### Gerenciamento de Clientes

- Cadastro de clientes.
- Listagem de todos os clientes.
- Busca de clientes por CPF.
- Busca de clientes por nome.
- Atualização de dados cadastrais.
- Exclusão de clientes.
- Validação de CPF, e-mail e telefone.
- Consulta de ingressos comprados por cliente utilizando JOIN.
- Relatório de quantidade de ingressos e total gasto por cliente.

### Gerenciamento de Filmes

- Cadastro de filmes.
- Listagem de todos os filmes.
- Busca de filmes por ID.
- Busca de filmes por título completo ou parcial.
- Atualização de dados dos filmes.
- Exclusão de filmes com confirmação.
- Validação de título, gênero, duração e classificação indicativa.
- Exibição organizada dos dados dos filmes.

### Gerenciamento de Ingressos

- Cadastro e venda de ingressos.
- Listagem de todos os ingressos.
- Busca de ingressos por ID.
- Busca de ingressos por cliente.
- Busca de ingressos por filme.
- Atualização de ingressos.
- Exclusão de ingressos com confirmação.
- Validação de clientes e filmes existentes.
- Validação de valores, assentos e datas das sessões.
- Prevenção de venda duplicada de assentos.

### Menu Principal

- Integração dos três módulos em uma única interface de terminal.
- Navegação entre os menus.
- Tratamento de opções inválidas.
- Encerramento controlado do sistema.

## Tecnologias Utilizadas

| Tecnologia | Finalidade |
| :--- | :--- |
| Python 3 | Desenvolvimento da lógica e das funcionalidades do sistema |
| MySQL | Armazenamento e gerenciamento dos dados |
| MySQL Workbench | Criação, administração e consulta do banco de dados |
| MySQL Connector/Python | Comunicação entre Python e MySQL |
| Python-dotenv | Carregamento das variáveis de ambiente |
| Visual Studio Code | Desenvolvimento e edição do código-fonte |
| Git | Controle de versões do projeto |
| GitHub | Hospedagem do repositório e desenvolvimento colaborativo |
| GitHub Desktop | Gerenciamento de commits e sincronização do repositório |
| Markdown | Documentação do projeto |

## Estrutura de Arquivos do Projeto

| Arquivo | Responsabilidade |
| :--- | :--- |
| `main.py` | Menu principal e integração dos módulos do sistema |
| `conexao.py` | Configuração e conexão com o banco de dados MySQL |
| `clientes.py` | CRUD de clientes, consultas e relatórios de gastos |
| `filmes.py` | CRUD de filmes, validações e menu de gerenciamento |
| `ingressos.py` | CRUD de ingressos, validações e controle de assentos |
| `validacoes.py` | Funções auxiliares de validação e formatação de dados |
| `schema.sql` | Criação do banco de dados, tabelas e restrições de integridade |
| `teste_filmes.py` | Testes das operações CRUD de filmes |
| `testes_ingressos.py` | Testes das operações de gerenciamento de ingressos |
| `testes_validacoes_filmes.py` | Testes das validações dos dados dos filmes |
| `.env` | Armazenamento local das configurações de acesso ao banco de dados |
| `.gitignore` | Definição dos arquivos que não devem ser enviados ao repositório |
| `.gitattributes` | Configuração de atributos dos arquivos no Git |
| `README.md` | Documentação geral do projeto |

**Observação:** O arquivo `.env` é de uso local e não deve ser enviado ao GitHub, pois contém informações de acesso ao banco de dados.

## Instalação e Configuração

### Pré-requisitos

- Python 3 instalado.
- MySQL Server instalado e em execução.
- MySQL Workbench.
- Git ou GitHub Desktop.
- Visual Studio Code (recomendado).

### 1. Obter o projeto

Clone o repositório pelo GitHub Desktop ou pelo Git e abra a pasta do projeto no Visual Studio Code.

### 2. Instalar as dependências

Abra o terminal na pasta do projeto e execute:

```bash
python -m pip install mysql-connector-python python-dotenv
```

### 3. Configurar o banco de dados

- Abra o MySQL Workbench.
- Conecte-se ao servidor MySQL local.
- Abra o arquivo `schema.sql`.
- Execute todo o script SQL.
- Verifique se o banco `gerenciamento_cinema` e suas três tabelas foram criados.

Caso o banco já tenha sido criado com uma versão anterior do projeto, verifique se a restrição `uq_assento_sessao` está presente na tabela `ingressos`.
Para verificar se a restrição existe, execute no MySQL Workbench:

```sql
USE gerenciamento_cinema;

SHOW INDEX FROM ingressos
WHERE Key_name = 'uq_assento_sessao';
```

Caso a consulta não retorne registros, execute:

```sql
ALTER TABLE ingressos
ADD CONSTRAINT uq_assento_sessao
UNIQUE (id_filme, assento, data_sessao);
```

Se existirem assentos duplicados para o mesmo filme, data e horário, será necessário corrigir esses registros antes de adicionar a restrição.

**Observação:** Esse procedimento é necessário apenas para bancos de dados antigos que ainda não possuem essa restrição.


### 4. Configurar as variáveis de ambiente

Crie um arquivo chamado `.env` na pasta principal do projeto com o seguinte conteúdo:

```env
DB_HOST=localhost
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_NAME=gerenciamento_cinema
```

Substitua os valores de usuário e senha pelas credenciais do seu servidor MySQL.

O usuário configurado deve possuir permissões de consulta, inserção, atualização e exclusão no banco de dados.

**Importante:** Nunca compartilhe suas credenciais de acesso nem envie o arquivo `.env` ao GitHub.

## Como Executar o Sistema

Após instalar as dependências e configurar o banco de dados e as variáveis de ambiente, abra o terminal na pasta principal do projeto e execute:

```bash
python main.py
```

O sistema apresentará o seguinte menu principal:

```text
================================
   SISTEMA DE GERENCIAMENTO
          DE CINEMA
================================
1. Gerenciar filmes
2. Gerenciar clientes
3. Gerenciar ingressos
0. Sair
```

### Navegação pelo Sistema

- Opção 1: acessa o módulo de gerenciamento de filmes.
- Opção 2: acessa o módulo de gerenciamento de clientes.
- Opção 3: acessa o módulo de gerenciamento de ingressos.
- Opção 0: encerra o sistema.

Dentro de cada módulo, o usuário poderá realizar as operações disponíveis e utilizar a opção 0 para retornar ao menu principal.

### Ordem Recomendada de Utilização

1. Cadastrar os clientes.
2. Cadastrar os filmes.
3. Cadastrar os ingressos vinculados aos clientes e filmes existentes.
4. Realizar consultas, atualizações e relatórios.
5. Encerrar o sistema pela opção 0 do menu principal.

Essa ordem respeita os relacionamentos e as restrições de integridade do banco de dados.

## Testes Realizados

Durante o desenvolvimento, foram realizados testes funcionais, testes de validação e testes de integração com o banco de dados MySQL.

### Testes do Módulo de Filmes

- Cadastro de filmes.
- Listagem dos filmes cadastrados.
- Busca por ID e por título completo ou parcial.
- Atualização dos dados.
- Exclusão com confirmação e cancelamento.
- Validação de títulos e gêneros vazios.
- Validação de duração negativa, igual a zero ou em formato inválido.
- Validação da classificação indicativa.
- Tratamento de IDs inválidos e inexistentes.

### Testes do Módulo de Ingressos

- Cadastro e listagem de ingressos.
- Busca por ID, cliente e filme.
- Atualização e exclusão de ingressos.
- Validação de clientes e filmes existentes.
- Validação de valores, assentos e datas.
- Bloqueio de venda duplicada de assentos.
- Confirmação e cancelamento de exclusões.

### Testes do Módulo de Clientes

- Listagem dos clientes cadastrados.
- Consulta de ingressos comprados por cliente utilizando JOIN.
- Relatório de quantidade de ingressos e total de gastos por cliente.

### Testes de Integração

- Inicialização do sistema pelo arquivo `main.py`.
- Acesso aos três módulos pelo menu principal.
- Comunicação entre Python e MySQL.
- Retorno dos módulos ao menu principal.
- Tratamento de opções inválidas.
- Encerramento controlado do sistema.

### Arquivos de Teste

| Arquivo | Finalidade |
| :--- | :--- |
| `teste_filmes.py` | Testar as operações CRUD de filmes |
| `testes_ingressos.py` | Testar as operações de gerenciamento de ingressos |
| `testes_validacoes_filmes.py` | Testar as regras de validação dos filmes |

**Atenção:** Alguns scripts de teste realizam inserções, atualizações e exclusões no banco de dados. Recomenda-se executá-los em um ambiente de testes.

### Resultados

Os testes realizados demonstraram o funcionamento das operações avaliadas, das validações implementadas e da integração entre os módulos do sistema e o banco de dados.