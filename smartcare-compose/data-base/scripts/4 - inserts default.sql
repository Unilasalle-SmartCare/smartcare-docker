\c smartcare_db;

SET ROLE SMARTCARE;

-- TIPODISPOSITIVO

INSERT INTO 
TIPODISPOSITIVO (NOME, IND_SIT)
VALUES ('Atuador', 1);

INSERT INTO 
TIPODISPOSITIVO (NOME, IND_SIT)
VALUES ('Sensor', 1);

-- DISPOSITIVO

INSERT INTO 
DISPOSITIVO (CODIGODISPOSITIVO, IDTIPO, IDAMBIENTE, NOME, DESCRICAO, EIXO_X, EIXO_Y, ORIENTACAO, IND_SIT)
VALUES ('BTN-01', 2, 1, 'Botão', 'Usado para detectar uma pessoa deitada na cama', 4.9, -5.4, '-Z', 1);

INSERT INTO 
DISPOSITIVO (CODIGODISPOSITIVO, IDTIPO, IDAMBIENTE, NOME, DESCRICAO, EIXO_X, EIXO_Y, ORIENTACAO, IND_SIT)
VALUES ('PIR-01', 2, 1, 'Sensor de Presença', 'Usado para detectar Presença', 4.5, -5.1, '-Z', 1);

INSERT INTO 
DISPOSITIVO (CODIGODISPOSITIVO, IDTIPO, IDAMBIENTE, NOME, DESCRICAO, EIXO_X, EIXO_Y, ORIENTACAO, IND_SIT)
VALUES ('PIR-02', 2, 2, 'Sensor de Presença', 'Usado para detectar Presença', 1.75, -5.1, '-Z', 1);

INSERT INTO 
DISPOSITIVO (CODIGODISPOSITIVO, IDTIPO, IDAMBIENTE, NOME, DESCRICAO, EIXO_X, EIXO_Y, ORIENTACAO, IND_SIT)
VALUES ('PIR-03', 2, 3, 'Sensor de Presença', 'Usado para detectar Presença', 1.5, -1.7, '-Z', 1);

INSERT INTO 
DISPOSITIVO (CODIGODISPOSITIVO, IDTIPO, IDAMBIENTE, NOME, DESCRICAO, EIXO_X, EIXO_Y, ORIENTACAO, IND_SIT)
VALUES ('PIR-04', 2, 4, 'Sensor de Presença', 'Usado para detectar Presença', 8.45,  -1.45, '-Z', 1);

INSERT INTO 
DISPOSITIVO (CODIGODISPOSITIVO, IDTIPO, IDAMBIENTE, NOME, DESCRICAO, EIXO_X, EIXO_Y, ORIENTACAO, IND_SIT)
VALUES ('PIR-05', 2, 5, 'Sensor de Presença', 'Usado para detectar Presença', 3.7, -3.2, '-Z', 1);

INSERT INTO 
DISPOSITIVO (CODIGODISPOSITIVO, IDTIPO, IDAMBIENTE, NOME, DESCRICAO, EIXO_X, EIXO_Y, ORIENTACAO, IND_SIT)
VALUES ('PIR-06', 2, 6, 'Sensor de Presença', 'Usado para detectar Presença', 5.75, -1.45, '-Z', 1);

INSERT INTO 
DISPOSITIVO (CODIGODISPOSITIVO, IDTIPO, IDAMBIENTE, NOME, DESCRICAO, EIXO_X, EIXO_Y, ORIENTACAO, IND_SIT)
VALUES ('PIR-07', 2, 7, 'Sensor de Presença', 'Usado para detectar Presença', 3.95, -1.45, '-Z', 1);

INSERT INTO 
DISPOSITIVO (CODIGODISPOSITIVO, IDTIPO, IDAMBIENTE, NOME, DESCRICAO, EIXO_X, EIXO_Y, ORIENTACAO, IND_SIT)
VALUES ('UIR-11', 2, 1, 'Ultrassônico',  'Usado para detectar a distância de um objeto ou pessoa', 4.50,  -5.10, '+Y', 1);

INSERT INTO 
DISPOSITIVO (CODIGODISPOSITIVO, IDTIPO, IDAMBIENTE, NOME, DESCRICAO, EIXO_X, EIXO_Y, ORIENTACAO, IND_SIT)
VALUES ('UIR-12', 2, 1, 'Ultrassônico',  'Usado para detectar a distância de um objeto ou pessoa', 4.15,  -4.00, '-X', 1);

INSERT INTO 
DISPOSITIVO (CODIGODISPOSITIVO, IDTIPO, IDAMBIENTE, NOME, DESCRICAO, EIXO_X, EIXO_Y, ORIENTACAO, IND_SIT)
VALUES ('UIR-21', 2, 2, 'Ultrassônico',  'Usado para detectar a distância de um objeto ou pessoa', 1.75,  -5.10, '-Y', 1);

INSERT INTO 
DISPOSITIVO (CODIGODISPOSITIVO, IDTIPO, IDAMBIENTE, NOME, DESCRICAO, EIXO_X, EIXO_Y, ORIENTACAO, IND_SIT)
VALUES ('UIR-22', 2, 2, 'Ultrassônico',  'Usado para detectar a distância de um objeto ou pessoa', 2.30,  -4.00, '+X', 1);

INSERT INTO 
DISPOSITIVO (CODIGODISPOSITIVO, IDTIPO, IDAMBIENTE, NOME, DESCRICAO, EIXO_X, EIXO_Y, ORIENTACAO, IND_SIT)
VALUES ('UIR-31', 2, 3, 'Ultrassônico',  'Usado para detectar a distância de um objeto ou pessoa', 0.00,  -1.70, '+X', 1);

INSERT INTO 
DISPOSITIVO (CODIGODISPOSITIVO, IDTIPO, IDAMBIENTE, NOME, DESCRICAO, EIXO_X, EIXO_Y, ORIENTACAO, IND_SIT)
VALUES ('UIR-32', 2, 3, 'Ultrassônico',  'Usado para detectar a distância de um objeto ou pessoa', 2.30,  -3.20, '+X', 1);

INSERT INTO 
DISPOSITIVO (CODIGODISPOSITIVO, IDTIPO, IDAMBIENTE, NOME, DESCRICAO, EIXO_X, EIXO_Y, ORIENTACAO, IND_SIT)
VALUES ('UIR-41', 2, 4, 'Ultrassônico',  'Usado para detectar a distância de um objeto ou pessoa', 6.50,  -2.65, '+X', 1);

INSERT INTO 
DISPOSITIVO (CODIGODISPOSITIVO, IDTIPO, IDAMBIENTE, NOME, DESCRICAO, EIXO_X, EIXO_Y, ORIENTACAO, IND_SIT)
VALUES ('UIR-42', 2, 4, 'Ultrassônico',  'Usado para detectar a distância de um objeto ou pessoa', 6.50,  -1.05, '+X', 1);

INSERT INTO 
DISPOSITIVO (CODIGODISPOSITIVO, IDTIPO, IDAMBIENTE, NOME, DESCRICAO, EIXO_X, EIXO_Y, ORIENTACAO, IND_SIT)
VALUES ('UIR-43', 2, 4, 'Ultrassônico',  'Usado para detectar a distância de um objeto ou pessoa', 7.40,  0.00, '-Y', 1);

INSERT INTO 
DISPOSITIVO (CODIGODISPOSITIVO, IDTIPO, IDAMBIENTE, NOME, DESCRICAO, EIXO_X, EIXO_Y, ORIENTACAO, IND_SIT)
VALUES ('UIR-44', 2, 4, 'Ultrassônico',  'Usado para detectar a distância de um objeto ou pessoa', 8.60,  0.00, '-Y', 1);

INSERT INTO 
DISPOSITIVO (CODIGODISPOSITIVO, IDTIPO, IDAMBIENTE, NOME, DESCRICAO, EIXO_X, EIXO_Y, ORIENTACAO, IND_SIT)
VALUES ('UIR-45', 2, 4, 'Ultrassônico',  'Usado para detectar a distância de um objeto ou pessoa', 9.80,  0.00, '-Y', 1);

INSERT INTO 
DISPOSITIVO (CODIGODISPOSITIVO, IDTIPO, IDAMBIENTE, NOME, DESCRICAO, EIXO_X, EIXO_Y, ORIENTACAO, IND_SIT)
VALUES ('UIR-46', 2, 4, 'Ultrassônico',  'Usado para detectar a distância de um objeto ou pessoa', 10.30,  -1.05, '-X', 1);

INSERT INTO 
DISPOSITIVO (CODIGODISPOSITIVO, IDTIPO, IDAMBIENTE, NOME, DESCRICAO, EIXO_X, EIXO_Y, ORIENTACAO, IND_SIT)
VALUES ('UIR-47', 2, 4, 'Ultrassônico',  'Usado para detectar a distância de um objeto ou pessoa', 10.30,  -2.05, '-X', 1);

INSERT INTO 
DISPOSITIVO (CODIGODISPOSITIVO, IDTIPO, IDAMBIENTE, NOME, DESCRICAO, EIXO_X, EIXO_Y, ORIENTACAO, IND_SIT)
VALUES ('UIR-48', 2, 4, 'Ultrassônico',  'Usado para detectar a distância de um objeto ou pessoa', 8.60,  -3.50, '+Y', 1);

INSERT INTO 
DISPOSITIVO (CODIGODISPOSITIVO, IDTIPO, IDAMBIENTE, NOME, DESCRICAO, EIXO_X, EIXO_Y, ORIENTACAO, IND_SIT)
VALUES ('UIR-49', 2, 4, 'Ultrassônico',  'Usado para detectar a distância de um objeto ou pessoa', 7.40,  -3.50, '+Y', 1);

INSERT INTO 
DISPOSITIVO (CODIGODISPOSITIVO, IDTIPO, IDAMBIENTE, NOME, DESCRICAO, EIXO_X, EIXO_Y, ORIENTACAO, IND_SIT)
VALUES ('UIR-50', 2, 5, 'Ultrassônico',  'Usado para detectar a distância de um objeto ou pessoa', 6.20,  -3.50, '+Y', 1);

INSERT INTO 
DISPOSITIVO (CODIGODISPOSITIVO, IDTIPO, IDAMBIENTE, NOME, DESCRICAO, EIXO_X, EIXO_Y, ORIENTACAO, IND_SIT)
VALUES ('UIR-51', 2, 5, 'Ultrassônico',  'Usado para detectar a distância de um objeto ou pessoa', 5.00,  -3.50, '+Y', 1);

INSERT INTO 
DISPOSITIVO (CODIGODISPOSITIVO, IDTIPO, IDAMBIENTE, NOME, DESCRICAO, EIXO_X, EIXO_Y, ORIENTACAO, IND_SIT)
VALUES ('UIR-52', 2, 5, 'Ultrassônico',  'Usado para detectar a distância de um objeto ou pessoa', 3.45,  -2.75, '-Y', 1);

INSERT INTO 
DISPOSITIVO (CODIGODISPOSITIVO, IDTIPO, IDAMBIENTE, NOME, DESCRICAO, EIXO_X, EIXO_Y, ORIENTACAO, IND_SIT)
VALUES ('UIR-53', 2, 5, 'Ultrassônico',  'Usado para detectar a distância de um objeto ou pessoa', 5.55,  -2.75, '-Y', 1);

INSERT INTO 
DISPOSITIVO (CODIGODISPOSITIVO, IDTIPO, IDAMBIENTE, NOME, DESCRICAO, EIXO_X, EIXO_Y, ORIENTACAO, IND_SIT)
VALUES ('UIR-61', 2, 6, 'Ultrassônico',  'Usado para detectar a distância de um objeto ou pessoa', 5.15,  -0.25, '+X', 1);

INSERT INTO 
DISPOSITIVO (CODIGODISPOSITIVO, IDTIPO, IDAMBIENTE, NOME, DESCRICAO, EIXO_X, EIXO_Y, ORIENTACAO, IND_SIT)
VALUES ('UIR-62', 2, 6, 'Ultrassônico',  'Usado para detectar a distância de um objeto ou pessoa', 5.15,  -1.10, '+X', 1);

INSERT INTO 
DISPOSITIVO (CODIGODISPOSITIVO, IDTIPO, IDAMBIENTE, NOME, DESCRICAO, EIXO_X, EIXO_Y, ORIENTACAO, IND_SIT)
VALUES ('UIR-63', 2, 6, 'Ultrassônico',  'Usado para detectar a distância de um objeto ou pessoa', 5.15,  -2.10, '+X', 1); 

INSERT INTO 
DISPOSITIVO (CODIGODISPOSITIVO, IDTIPO, IDAMBIENTE, NOME, DESCRICAO, EIXO_X, EIXO_Y, ORIENTACAO, IND_SIT)
VALUES ('UIR-71', 2, 7, 'Ultrassônico',  'Usado para detectar a distância de um objeto ou pessoa', 4.50,  -0.45, '-X', 1);

INSERT INTO 
DISPOSITIVO (CODIGODISPOSITIVO, IDTIPO, IDAMBIENTE, NOME, DESCRICAO, EIXO_X, EIXO_Y, ORIENTACAO, IND_SIT)
VALUES ('UIR-72', 2, 7, 'Ultrassônico',  'Usado para detectar a distância de um objeto ou pessoa', 4.50,  -1.10, '-X', 1);

INSERT INTO 
DISPOSITIVO (CODIGODISPOSITIVO, IDTIPO, IDAMBIENTE, NOME, DESCRICAO, EIXO_X, EIXO_Y, ORIENTACAO, IND_SIT)
VALUES ('UIR-73', 2, 7, 'Ultrassônico',  'Usado para detectar a distância de um objeto ou pessoa', 3.65,  -2.10, '+X', 1);

-- AMBIENTE

INSERT INTO 
AMBIENTE (NOME, DESCRICAO, IND_SIT)
VALUES ('Quarto 01', '', 1);

INSERT INTO 
AMBIENTE (NOME, DESCRICAO, IND_SIT)
VALUES ('Quarto 02', '', 1);

INSERT INTO 
AMBIENTE (NOME, DESCRICAO, IND_SIT)
VALUES ('Quarto 03', '', 1);

INSERT INTO 
AMBIENTE (NOME, DESCRICAO, IND_SIT)
VALUES ('Sala', '', 1);

INSERT INTO 
AMBIENTE (NOME, DESCRICAO, IND_SIT)
VALUES ('Circulação', '', 1);

INSERT INTO 
AMBIENTE (NOME, DESCRICAO, IND_SIT)
VALUES ('Cozinha', '', 1);

INSERT INTO 
AMBIENTE (NOME, DESCRICAO, IND_SIT)
VALUES ('Banheiro', '', 1);