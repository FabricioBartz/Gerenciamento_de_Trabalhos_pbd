CREATE SCHEMA gerenciamento_trabalhos;

SET search_path TO gerenciamento_trabalhos;

CREATE TABLE Curso (
    id_curso INTEGER,
    nome VARCHAR(100) NOT NULL,
    coordenador VARCHAR(100) NOT NULL,
    departamento VARCHAR(100) NOT NULL,
    PRIMARY KEY (id_curso)
);

CREATE TABLE Professor (
    id_professor INTEGER,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    id_curso INTEGER NOT NULL,
    FOREIGN KEY (id_curso) REFERENCES Curso(id_curso),
    PRIMARY KEY (id_professor)
);

CREATE TABLE Aluno (
    id_aluno INTEGER,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    id_curso INTEGER NOT NULL,
    id_professor INTEGER NOT NULL,
    FOREIGN KEY (id_curso) REFERENCES Curso(id_curso),
    FOREIGN KEY (id_professor) REFERENCES Professor(id_professor),
    PRIMARY KEY (id_aluno)
);

CREATE TABLE Funcionario (
    id_funcionario INTEGER,
    nome VARCHAR(100) NOT NULL,
    cargo VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    PRIMARY KEY (id_funcionario)
);

CREATE TABLE Trabalho_Academico (
    id_trabalho INTEGER,
    titulo VARCHAR(150) NOT NULL,
    data_submissao DATE NOT NULL,
    id_aluno INTEGER NOT NULL,
    id_professor INTEGER NOT NULL,
    FOREIGN KEY (id_aluno) REFERENCES Aluno(id_aluno),
    FOREIGN KEY (id_professor) REFERENCES Professor(id_professor),
    PRIMARY KEY (id_trabalho)
);

CREATE TABLE Tipo_Etapa (
    id_tipo_etapa INTEGER,
    nome VARCHAR(100) NOT NULL,
    PRIMARY KEY (id_tipo_etapa)
);

CREATE TABLE Etapa (
    id_etapa INTEGER,
    prazo DATE NOT NULL,
    status VARCHAR(50) NOT NULL,
    id_trabalho INTEGER NOT NULL,
    id_funcionario INTEGER NOT NULL,
    id_tipo_etapa INTEGER NOT NULL,
    PRIMARY KEY (id_etapa),
    FOREIGN KEY (id_trabalho) REFERENCES Trabalho_Academico(id_trabalho),
    FOREIGN KEY (id_funcionario) REFERENCES Funcionario(id_funcionario),
    FOREIGN KEY (id_tipo_etapa) REFERENCES Tipo_Etapa(id_tipo_etapa)
);


CREATE TABLE Publicador (
    id_publicador INTEGER,
    nome VARCHAR(100) NOT NULL,
    PRIMARY KEY (id_publicador)
);

CREATE TABLE Comite_Etica (
    id_comite INTEGER,
    nome VARCHAR(100) NOT NULL,
    departamento VARCHAR(100) NOT NULL,
    PRIMARY KEY (id_comite)
);

CREATE TABLE Submete (
    id_aluno INTEGER NOT NULL,
    id_trabalho INTEGER NOT NULL,
    FOREIGN KEY (id_aluno) REFERENCES Aluno(id_aluno),
    FOREIGN KEY (id_trabalho) REFERENCES Trabalho_Academico(id_trabalho),
    PRIMARY KEY (id_aluno, id_trabalho)
);

CREATE TABLE Avalia (
    id_trabalho INTEGER NOT NULL,
    id_professor INTEGER NOT NULL,
    FOREIGN KEY (id_trabalho) REFERENCES Trabalho_Academico(id_trabalho),
    FOREIGN KEY (id_professor) REFERENCES Professor(id_professor),
    PRIMARY KEY (id_trabalho, id_professor)
);

CREATE TABLE Aprova (
    id_trabalho INTEGER NOT NULL,
    id_publicador INTEGER NOT NULL,
    data DATE NOT NULL,
    FOREIGN KEY (id_trabalho) REFERENCES Trabalho_Academico(id_trabalho),
    FOREIGN KEY (id_publicador) REFERENCES Publicador(id_publicador),
    PRIMARY KEY (id_trabalho, id_publicador)
);
