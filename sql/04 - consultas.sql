-- consultas

-- 1. Listar os Trabalhos, alunos que submeteram e seus orientadores (JOIN entre Aluno, Trabalho_Academico e Professor)

SELECT 
    t.titulo AS titulo_trabalho,
    a.nome AS nome_aluno,
    p.nome AS nome_orientador
FROM Trabalho_Academico t
JOIN Aluno a ON t.id_aluno = a.id_aluno
JOIN Professor p ON t.id_professor = p.id_professor;


-- 2. Mostrar o orientador com mais trabalhos (JOIN entre Trabalho_Academico e Professor)
WITH contagem AS (
    SELECT 
        p.nome AS orientador,
        COUNT(t.id_trabalho) AS total_trabalhos
    FROM Professor p
    JOIN Trabalho_Academico t ON p.id_professor = t.id_professor
    GROUP BY p.nome
)
SELECT *
FROM contagem
WHERE total_trabalhos = (SELECT MAX(total_trabalhos) FROM contagem);



-- 3. Perfil completo de um aluno por ID (JOIN entre Aluno, Submete, Trabalho_Academico e Professor)
SELECT 
    a.nome AS nome_aluno,
    t.titulo AS titulo_trabalho,
    p.nome AS nome_orientador
FROM Aluno a
JOIN Submete s ON s.id_aluno = a.id_aluno
JOIN Trabalho_Academico t ON t.id_trabalho = s.id_trabalho
JOIN Professor p ON t.id_professor = p.id_professor
WHERE 
    a.id_aluno = 20180001;  -- substitua pelo ID do aluno desejado


-- 4. Listar os publicadores e os trabalhos aprovados por eles, com data de aprovação (JOIN entre Aprova, Publicador e Trabalho_Academico)
SELECT pub.nome AS publicador, t.titulo AS trabalho, a.data
FROM Aprova a
JOIN Publicador pub ON a.id_publicador = pub.id_publicador
JOIN Trabalho_Academico t ON a.id_trabalho = t.id_trabalho
ORDER BY pub.nome, a.data;

-- 5. Consultar os avaliadores e o nome dos trabalhos que eles avaliaram (JOIN entre Trabalho_Academico, Avalia, Professor)
SELECT 
    p.nome AS nome_avaliador,
    ta.titulo AS titulo_trabalho
FROM 
    Avalia a
JOIN 
    Trabalho_Academico ta ON a.id_trabalho = ta.id_trabalho
JOIN 
    Professor p ON a.id_professor = p.id_professor
ORDER BY p.nome;


--6 Consultar os trabalhos acadêmicos que pertencem a um determinado curso (JOIN entre Trabalho_Academico, Aluno e Curso)
SELECT 
    t.titulo AS titulo_trabalho,
    a.nome AS nome_aluno,
    c.nome AS nome_curso
FROM 
    Trabalho_Academico t
JOIN Aluno a ON t.id_aluno = a.id_aluno
JOIN Curso c ON a.id_curso = c.id_curso
WHERE 
    c.nome = 'Ciência da Computação';  -- substitua pelo nome do curso desejado

--7 Consultar Trabalhos em uma etapa específica, por nome em Tipo_Etapa (JOIN entre Etapa, Tipo_Etapa e Trabalho_Academico)
SELECT 
    ta.titulo AS titulo_trabalho,
    te.nome AS nome_etapa,
    e.status,
    e.prazo
FROM 
    Etapa e
JOIN 
    Tipo_Etapa te ON e.id_tipo_etapa = te.id_tipo_etapa
JOIN 
    Trabalho_Academico ta ON e.id_trabalho = ta.id_trabalho
WHERE 
    te.nome = 'Submissão';  -- substitua pelo nome da etapa desejada

--8 Visualizar uma tabela

SELECT * FROM nome_da_tabela;

SELECT * FROM curso;
SELECT * FROM aluno;
SELECT * FROM professor;
SELECT * FROM funcionario;
SELECT * FROM trabalho_academico;
SELECT * FROM tipo_etapa;
SELECT * FROM etapa;
SELECT * FROM submete;
SELECT * FROM avalia;
SELECT * FROM aprova;
SELECT * FROM comite_etica;
SELECT * FROM publicador;

--9 Para testar a Trigger (INSERT)

INSERT INTO Avalia (id_trabalho, id_professor) VALUES (1, 1);

