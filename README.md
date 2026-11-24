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