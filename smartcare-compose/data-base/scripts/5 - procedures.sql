\c smartcare_db;

SET ROLE SMARTCARE;

-- PROCEDURE: public.usp_insere_medicao(character varying, timestamp without time zone, character varying, character)

-- DROP PROCEDURE IF EXISTS public.usp_insere_medicao(character varying, timestamp without time zone, character varying, character);

CREATE OR REPLACE PROCEDURE public.usp_insere_medicao(
	codigo_dispositivo character varying,
	data_hora timestamp without time zone,
	valor character varying,
	unidade character)
LANGUAGE 'plpgsql'
AS $BODY$
BEGIN

	WITH DISPOSITIVO_CODIGO (IDDISPOSITIVO) AS (
        SELECT
            D.IDDISPOSITIVO AS IDDISPOSITIVO
        FROM    DISPOSITIVO D
        WHERE   1 = 1
				AND EXISTS(SELECT 1 FROM DISPOSITIVO WHERE CODIGODISPOSITIVO = CODIGO_DISPOSITIVO)
            AND D.CODIGODISPOSITIVO = CODIGO_DISPOSITIVO
		LIMIT	1
    )
	
	INSERT	INTO DISPOSITIVO (CODIGODISPOSITIVO, IND_SIT)
	SELECT
		CODIGO_DISPOSITIVO ,
		3
	WHERE	NOT EXISTS(SELECT 1 FROM DISPOSITIVO_CODIGO);
	
	WITH DISPOSITIVO_CODIGO (IDDISPOSITIVO) AS (
        SELECT
            D.IDDISPOSITIVO AS IDDISPOSITIVO
        FROM    DISPOSITIVO D
        WHERE   1 = 1
				AND EXISTS(SELECT 1 FROM DISPOSITIVO WHERE CODIGODISPOSITIVO = CODIGO_DISPOSITIVO)
            AND D.CODIGODISPOSITIVO = CODIGO_DISPOSITIVO
		LIMIT	1
    )

    INSERT INTO MEDICAO (
                            IDDISPOSITIVO , 
                            DATAHORA , 
                            VALOR , 
                            UNIDADE , 
                            IND_SIT
                        )
    SELECT
        IDDISPOSITIVO ,
        DATA_HORA ,
        VALOR ,
        UNIDADE ,
		1
    FROM    DISPOSITIVO_CODIGO;
        
END;
    
    
    
    
$BODY$;
