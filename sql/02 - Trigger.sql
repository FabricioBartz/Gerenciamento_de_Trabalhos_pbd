-- Função que verifica se o professor avaliador é o mesmo orientador
CREATE OR REPLACE FUNCTION verifica_orientador_nao_avaliador()
RETURNS TRIGGER AS $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM Trabalho_Academico
        WHERE id_trabalho = NEW.id_trabalho AND id_professor = NEW.id_professor
    ) THEN
        RAISE EXCEPTION 'O professor orientador não pode ser avaliador do próprio trabalho.';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger que chama a função antes de inserir na tabela Avalia
CREATE TRIGGER trigger_verifica_orientador
BEFORE INSERT ON Avalia
FOR EACH ROW
EXECUTE FUNCTION verifica_orientador_nao_avaliador();
