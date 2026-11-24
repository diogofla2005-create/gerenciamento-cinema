CREATE DATABASE IF NOT EXISTS gerenciamento_cinema
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE gerenciamento_cinema;

-- Tabela 1: Clientes
CREATE TABLE IF NOT EXISTS clientes (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cpf CHAR(11) NOT NULL UNIQUE,
    email VARCHAR(120) NOT NULL UNIQUE,
    telefone VARCHAR(11) NOT NULL,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- Tabela 2: Filmes
CREATE TABLE IF NOT EXISTS filmes (
    id_filme INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(150) NOT NULL,
    genero VARCHAR(50) NOT NULL,
    duracao_min INT NOT NULL,
    classificacao VARCHAR(10) NOT NULL
) ENGINE=InnoDB;

-- Tabela 3: Ingressos (Relacionamento 1:N)
CREATE TABLE IF NOT EXISTS ingressos (
    id_ingresso INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT NOT NULL,
    id_filme INT NOT NULL,
    assento VARCHAR(10) NOT NULL,
    valor DECIMAL(6, 2) NOT NULL,
    data_sessao DATETIME NOT NULL,
    CONSTRAINT fk_ingresso_cliente
        FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    CONSTRAINT fk_ingresso_filme
        FOREIGN KEY (id_filme) REFERENCES filmes(id_filme)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
) ENGINE=InnoDB;