-- Curso
INSERT INTO Curso (id_curso, nome, coordenador, departamento) VALUES
(1, 'Engenharia da Computação', 'Marcelo Porto', 'Centro de Desenvolvimento Tecnológico'),
(2, 'Ciência da Computação', 'Guilherme Netto', 'Centro de Desenvolvimento Tecnológico');

-- Professores
INSERT INTO Professor (id_professor, nome, email, id_curso) VALUES
(1, 'Ana Pernas', 'ana.pernas@universidade.com', 1),
(2, 'Marcelo Porto', 'marcelo.porto@universidade.com', 1),
(3, 'Marilton de Aguiar', 'marilton.aguiar@universidade.com', 1),
(4, 'Brenda Santana', 'brenda.santana@universidade.com', 2),
(5, 'Guilherme Corrêa', 'guilherme.correa@universidade.com', 2),
(6, 'Gerson Cavalheiro', 'gerson.cavalheiro@universidade.com', 2),
(7, 'Leomar Soares', 'leomar.soares@universidade.com', 1);

-- Funcionários
INSERT INTO Funcionario (id_funcionario, nome, cargo, email) VALUES
(1, 'Carlos Mendes', 'Secretário', 'carlos.mendes@universidade.com'),
(2, 'Luciana Prado', 'Coordenadora', 'luciana.prado@universidade.com');

-- Publicadores
INSERT INTO Publicador (id_publicador, nome) VALUES
(1, 'Revista Científica A'),
(2, 'Revista Acadêmica B');

-- Comitê de Ética
INSERT INTO Comite_Etica (id_comite, nome, departamento) VALUES
(1, 'Comitê Central de Ética', 'Pesquisas Humanas'),
(2, 'Comitê Científico', 'Tecnologia e Sociedade');

-- Alunos
INSERT INTO Aluno (id_aluno, nome, email, id_curso, id_professor) VALUES
(20180001, 'Lucas Pereira', 'lucas.pereira@aluno.com', 1, 1),
(20180134, 'Ricardo Lima', 'ricardo.lima@aluno.com', 1, 2),
(20200012, 'Tiago Silva', 'tiago.silva@aluno.com', 1, 3),
(20200333, 'Bruno Teixeira', 'bruno.teixeira@aluno.com', 1, 7),
(20180567, 'Paulo Henrique', 'paulo.henrique@aluno.com', 1, 1),
(20210456, 'Fabricio Bartz', 'fabricio.bartz@aluno.com', 2, 4),
(20190087, 'Arthur Soares', 'arthur.soares@aluno.com', 2, 5),
(20210145, 'Valtair Souza', 'valtair.souza@aluno.com', 2, 6),
(20190222, 'Aline Martins', 'aline.martins@aluno.com', 2, 5),
(20220678, 'Juliana Barros', 'juliana.barros@aluno.com', 2, 4);

-- Tipo de Etapa
INSERT INTO Tipo_Etapa (id_tipo_etapa, nome) VALUES
(1, 'Submissão'),
(2, 'Avaliação'),
(3, 'Correções'),
(4, 'Aprovação'),
(5, 'Publicação'),
(6, 'Comitê de ética');

-- Trabalhos Acadêmicos 
INSERT INTO Trabalho_Academico (id_trabalho, titulo, data_submissao, id_aluno, id_professor) VALUES
(1, 'Sistemas Embarcados', '2022-08-15', 20200012, 3),
(2, 'Reconhecimento Facial com IA', '2023-03-10', 20180001, 1),
(3, 'Blockchain na Educação', '2023-09-22', 20180134, 2),
(4, 'Robótica Educacional', '2023-10-10', 20220678, 4),
(5, 'Detecção de Fake News', '2023-11-28', 20200333, 7),
(6, 'Big Data em Saúde', '2024-02-25', 20190222, 5),
(7, 'Cidades Inteligentes', '2024-04-01', 20210456, 4),
(8, 'Redes Neurais Aplicadas', '2024-05-12', 20190087, 5),
(9, 'Privacidade em IoT', '2025-01-18', 20210145, 6),
(10, 'Computação Quântica', '2025-02-05', 20180567, 1);

-- Etapas 
INSERT INTO Etapa (id_etapa, prazo, status, id_trabalho, id_funcionario, id_tipo_etapa) VALUES
(1, '2022-08-15', 'Concluído', 1, 1, 1),
(2, '2022-08-25', 'Concluído', 1, 1, 2),
(3, '2022-09-10', 'Concluído', 1, 1, 3),
(4, '2022-09-25', 'Concluído', 1, 1, 4),
(5, '2022-10-10', 'Concluído', 1, 1, 5),
(6, '2023-03-10', 'Concluído', 2, 1, 1),
(7, '2023-03-15', 'Concluído', 2, 1, 2),
(8, '2023-04-05', 'Concluído', 2, 2, 3),
(9, '2023-04-18', 'Concluído', 2, 1, 4),
(10, '2023-05-01', 'Concluído', 2, 2, 5),
(11, '2023-09-22', 'Concluído', 3, 2, 1),
(12, '2023-09-30', 'Concluído', 3, 1, 2),
(13, '2023-10-10', 'Concluído', 3, 1, 3),
(14, '2023-10-25', 'Concluído', 3, 1, 4),
(15, '2023-11-28', 'Concluído', 3, 1, 5),
(16, '2023-10-10', 'Concluído', 4, 1, 1),
(17, '2023-10-25', 'Concluído', 4, 1, 2),
(18, '2023-11-05', 'Concluído', 4, 2, 3),
(19, '2023-11-10', 'Concluído', 4, 2, 4),
(20, '2023-11-28', 'Concluído', 5, 1, 1),
(21, '2023-12-10', 'Pendente', 5, 1, 3),
(22, '2024-02-25', 'Concluído', 6, 2, 1),
(23, '2024-03-01', 'Concluído', 6, 2, 2),
(24, '2024-04-05', 'Concluído', 6, 1, 3),
(25, '2024-04-15', 'Concluído', 6, 1, 4),
(26, '2024-05-01', 'Concluído', 6, 2, 5),
(27, '2024-04-01', 'Concluído', 7, 2, 1),
(28, '2024-04-20', 'Concluído', 7, 1, 3),
(29, '2024-05-01', 'Concluído', 7, 2, 4),
(30, '2024-05-10', 'Concluído', 7, 1, 5),
(31, '2024-05-12', 'Concluído', 8, 2, 1),
(32, '2024-05-25', 'Pendente', 8, 2, 3),
(33, '2025-01-18', 'Concluído', 9, 1, 1),
(34, '2025-01-25', 'Concluído', 9, 2, 2),
(35, '2025-02-05', 'Concluído', 10, 1, 1),
(36, '2025-02-15', 'Pendente', 10, 1, 3);

-- Submete
INSERT INTO Submete (id_aluno, id_trabalho) VALUES
(20200012, 1),
(20180001, 2),
(20180134, 3),
(20220678, 4),
(20200333, 5),
(20190222, 6),
(20210456, 7),
(20190087, 8),
(20210145, 9),
(20180567, 10);

-- Avalia 
INSERT INTO Avalia (id_trabalho, id_professor) VALUES
(1, 1),
(2, 3),
(3, 7),
(4, 5),
(5, 2),
(6, 6),
(7, 1),
(8, 4),
(9, 5),
(10, 2);

-- Aprova 
INSERT INTO Aprova (id_trabalho, id_publicador, data) VALUES
(1, 2, '2022-10-10'),
(2, 1, '2023-05-01'),
(6, 2, '2024-05-01'),
(7, 1, '2024-05-10');
