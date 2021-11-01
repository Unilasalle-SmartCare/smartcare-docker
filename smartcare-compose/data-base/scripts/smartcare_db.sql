
CREATE DATABASE smartcare_db;

\c smartcare_db

CREATE TABLE TipoDispositivo 
(
  IdTipo SERIAL,
  Nome VARCHAR(40) NOT NULL,
  Ind_Sit INT,
  PRIMARY KEY (IdTipo)
);

INSERT INTO 
TipoDispositivo (Nome, Ind_Sit)
VALUES ('Atuador', 1);

INSERT INTO 
TipoDispositivo (Nome, Ind_Sit)
VALUES ('Sensor', 1);

CREATE TABLE Dispositivo 
(   
  IdDispositivo SERIAL PRIMARY KEY ,
  CodigoDispositivo VARCHAR(40) NULL ,
  IdTipo INT NULL ,
  IdAmbiente INT NULL ,
  Nome VARCHAR(40) NULL ,
  Descricao VARCHAR(200) NULL ,
  Eixo_X FLOAT NULL ,
  Eixo_Y FLOAT NULL ,
  Orientacao char(2) ,
  Ind_sit INT ,
  FOREIGN KEY (IdTipo) REFERENCES TipoDispositivo(IdTipo)
);

INSERT INTO 
Dispositivo (CodigoDispositivo, IdTipo, IdAmbiente, Nome, Descricao, Eixo_X, Eixo_Y, Orientacao, Ind_Sit)
VALUES ('BTN-01', 2, 1, 'Botão', 'Usado para detectar uma pessoa deitada na cama', 4.9, -5.4, '-Z', 1);

INSERT INTO 
Dispositivo (CodigoDispositivo, IdTipo, IdAmbiente, Nome, Descricao, Eixo_X, Eixo_Y, Orientacao, Ind_Sit)
VALUES ('PIR-01', 2, 1, 'Sensor de Presença', 'Usado para detectar Presença', 4.5, -5.1, '-Z', 1);

INSERT INTO 
Dispositivo (CodigoDispositivo, IdTipo, IdAmbiente, Nome, Descricao, Eixo_X, Eixo_Y, Orientacao, Ind_Sit)
VALUES ('PIR-02', 2, 2, 'Sensor de Presença', 'Usado para detectar Presença', 1.75, -5.1, '-Z', 1);

INSERT INTO 
Dispositivo (CodigoDispositivo, IdTipo, IdAmbiente, Nome, Descricao, Eixo_X, Eixo_Y, Orientacao, Ind_Sit)
VALUES ('PIR-03', 2, 3, 'Sensor de Presença', 'Usado para detectar Presença', 1.5, -1.7, '-Z', 1);

INSERT INTO 
Dispositivo (CodigoDispositivo, IdTipo, IdAmbiente, Nome, Descricao, Eixo_X, Eixo_Y, Orientacao, Ind_Sit)
VALUES ('PIR-04', 2, 4, 'Sensor de Presença', 'Usado para detectar Presença', 8.45,  -1.45, '-Z', 1);

INSERT INTO 
Dispositivo (CodigoDispositivo, IdTipo, IdAmbiente, Nome, Descricao, Eixo_X, Eixo_Y, Orientacao, Ind_Sit)
VALUES ('PIR-05', 2, 5, 'Sensor de Presença', 'Usado para detectar Presença', 3.7, -3.2, '-Z', 1);

INSERT INTO 
Dispositivo (CodigoDispositivo, IdTipo, IdAmbiente, Nome, Descricao, Eixo_X, Eixo_Y, Orientacao, Ind_Sit)
VALUES ('PIR-06', 2, 6, 'Sensor de Presença', 'Usado para detectar Presença', 5.75, -1.45, '-Z', 1);

INSERT INTO 
Dispositivo (CodigoDispositivo, IdTipo, IdAmbiente, Nome, Descricao, Eixo_X, Eixo_Y, Orientacao, Ind_Sit)
VALUES ('PIR-07', 2, 7, 'Sensor de Presença', 'Usado para detectar Presença', 3.95, -1.45, '-Z', 1);

INSERT INTO 
Dispositivo (CodigoDispositivo, IdTipo, IdAmbiente, Nome, Descricao, Eixo_X, Eixo_Y, Orientacao, Ind_Sit)
VALUES ('UIR-11', 2, 1, 'Ultrassônico',  'Usado para detectar a distância de um objeto ou pessoa', 4.50,  -5.10, '+Y', 1);

INSERT INTO 
Dispositivo (CodigoDispositivo, IdTipo, IdAmbiente, Nome, Descricao, Eixo_X, Eixo_Y, Orientacao, Ind_Sit)
VALUES ('UIR-12', 2, 1, 'Ultrassônico',  'Usado para detectar a distância de um objeto ou pessoa', 4.15,  -4.00, '-X', 1);

INSERT INTO 
Dispositivo (CodigoDispositivo, IdTipo, IdAmbiente, Nome, Descricao, Eixo_X, Eixo_Y, Orientacao, Ind_Sit)
VALUES ('UIR-21', 2, 2, 'Ultrassônico',  'Usado para detectar a distância de um objeto ou pessoa', 1.75,  -5.10, '-Y', 1);

INSERT INTO 
Dispositivo (CodigoDispositivo, IdTipo, IdAmbiente, Nome, Descricao, Eixo_X, Eixo_Y, Orientacao, Ind_Sit)
VALUES ('UIR-22', 2, 2, 'Ultrassônico',  'Usado para detectar a distância de um objeto ou pessoa', 2.30,  -4.00, '+X', 1);

INSERT INTO 
Dispositivo (CodigoDispositivo, IdTipo, IdAmbiente, Nome, Descricao, Eixo_X, Eixo_Y, Orientacao, Ind_Sit)
VALUES ('UIR-31', 2, 3, 'Ultrassônico',  'Usado para detectar a distância de um objeto ou pessoa', 0.00,  -1.70, '+X', 1);

INSERT INTO 
Dispositivo (CodigoDispositivo, IdTipo, IdAmbiente, Nome, Descricao, Eixo_X, Eixo_Y, Orientacao, Ind_Sit)
VALUES ('UIR-32', 2, 3, 'Ultrassônico',  'Usado para detectar a distância de um objeto ou pessoa', 2.30,  -3.20, '+X', 1);

INSERT INTO 
Dispositivo (CodigoDispositivo, IdTipo, IdAmbiente, Nome, Descricao, Eixo_X, Eixo_Y, Orientacao, Ind_Sit)
VALUES ('UIR-41', 2, 4, 'Ultrassônico',  'Usado para detectar a distância de um objeto ou pessoa', 6.50,  -2.65, '+X', 1);

INSERT INTO 
Dispositivo (CodigoDispositivo, IdTipo, IdAmbiente, Nome, Descricao, Eixo_X, Eixo_Y, Orientacao, Ind_Sit)
VALUES ('UIR-42', 2, 4, 'Ultrassônico',  'Usado para detectar a distância de um objeto ou pessoa', 6.50,  -1.05, '+X', 1);

INSERT INTO 
Dispositivo (CodigoDispositivo, IdTipo, IdAmbiente, Nome, Descricao, Eixo_X, Eixo_Y, Orientacao, Ind_Sit)
VALUES ('UIR-43', 2, 4, 'Ultrassônico',  'Usado para detectar a distância de um objeto ou pessoa', 7.40,  0.00, '-Y', 1);

INSERT INTO 
Dispositivo (CodigoDispositivo, IdTipo, IdAmbiente, Nome, Descricao, Eixo_X, Eixo_Y, Orientacao, Ind_Sit)
VALUES ('UIR-44', 2, 4, 'Ultrassônico',  'Usado para detectar a distância de um objeto ou pessoa', 8.60,  0.00, '-Y', 1);

INSERT INTO 
Dispositivo (CodigoDispositivo, IdTipo, IdAmbiente, Nome, Descricao, Eixo_X, Eixo_Y, Orientacao, Ind_Sit)
VALUES ('UIR-45', 2, 4, 'Ultrassônico',  'Usado para detectar a distância de um objeto ou pessoa', 9.80,  0.00, '-Y', 1);

INSERT INTO 
Dispositivo (CodigoDispositivo, IdTipo, IdAmbiente, Nome, Descricao, Eixo_X, Eixo_Y, Orientacao, Ind_Sit)
VALUES ('UIR-46', 2, 4, 'Ultrassônico',  'Usado para detectar a distância de um objeto ou pessoa', 10.30,  -1.05, '-X', 1);

INSERT INTO 
Dispositivo (CodigoDispositivo, IdTipo, IdAmbiente, Nome, Descricao, Eixo_X, Eixo_Y, Orientacao, Ind_Sit)
VALUES ('UIR-47', 2, 4, 'Ultrassônico',  'Usado para detectar a distância de um objeto ou pessoa', 10.30,  -2.05, '-X', 1);

INSERT INTO 
Dispositivo (CodigoDispositivo, IdTipo, IdAmbiente, Nome, Descricao, Eixo_X, Eixo_Y, Orientacao, Ind_Sit)
VALUES ('UIR-48', 2, 4, 'Ultrassônico',  'Usado para detectar a distância de um objeto ou pessoa', 8.60,  -3.50, '+Y', 1);

INSERT INTO 
Dispositivo (CodigoDispositivo, IdTipo, IdAmbiente, Nome, Descricao, Eixo_X, Eixo_Y, Orientacao, Ind_Sit)
VALUES ('UIR-49', 2, 4, 'Ultrassônico',  'Usado para detectar a distância de um objeto ou pessoa', 7.40,  -3.50, '+Y', 1);

INSERT INTO 
Dispositivo (CodigoDispositivo, IdTipo, IdAmbiente, Nome, Descricao, Eixo_X, Eixo_Y, Orientacao, Ind_Sit)
VALUES ('UIR-50', 2, 5, 'Ultrassônico',  'Usado para detectar a distância de um objeto ou pessoa', 6.20,  -3.50, '+Y', 1);

INSERT INTO 
Dispositivo (CodigoDispositivo, IdTipo, IdAmbiente, Nome, Descricao, Eixo_X, Eixo_Y, Orientacao, Ind_Sit)
VALUES ('UIR-51', 2, 5, 'Ultrassônico',  'Usado para detectar a distância de um objeto ou pessoa', 5.00,  -3.50, '+Y', 1);

INSERT INTO 
Dispositivo (CodigoDispositivo, IdTipo, IdAmbiente, Nome, Descricao, Eixo_X, Eixo_Y, Orientacao, Ind_Sit)
VALUES ('UIR-52', 2, 5, 'Ultrassônico',  'Usado para detectar a distância de um objeto ou pessoa', 3.45,  -2.75, '-Y', 1);

INSERT INTO 
Dispositivo (CodigoDispositivo, IdTipo, IdAmbiente, Nome, Descricao, Eixo_X, Eixo_Y, Orientacao, Ind_Sit)
VALUES ('UIR-53', 2, 5, 'Ultrassônico',  'Usado para detectar a distância de um objeto ou pessoa', 5.55,  -2.75, '-Y', 1);

INSERT INTO 
Dispositivo (CodigoDispositivo, IdTipo, IdAmbiente, Nome, Descricao, Eixo_X, Eixo_Y, Orientacao, Ind_Sit)
VALUES ('UIR-61', 2, 6, 'Ultrassônico',  'Usado para detectar a distância de um objeto ou pessoa', 5.15,  -0.25, '+X', 1);

INSERT INTO 
Dispositivo (CodigoDispositivo, IdTipo, IdAmbiente, Nome, Descricao, Eixo_X, Eixo_Y, Orientacao, Ind_Sit)
VALUES ('UIR-62', 2, 6, 'Ultrassônico',  'Usado para detectar a distância de um objeto ou pessoa', 5.15,  -1.10, '+X', 1);

INSERT INTO 
Dispositivo (CodigoDispositivo, IdTipo, IdAmbiente, Nome, Descricao, Eixo_X, Eixo_Y, Orientacao, Ind_Sit)
VALUES ('UIR-63', 2, 6, 'Ultrassônico',  'Usado para detectar a distância de um objeto ou pessoa', 5.15,  -2.10, '+X', 1); 

INSERT INTO 
Dispositivo (CodigoDispositivo, IdTipo, IdAmbiente, Nome, Descricao, Eixo_X, Eixo_Y, Orientacao, Ind_Sit)
VALUES ('UIR-71', 2, 7, 'Ultrassônico',  'Usado para detectar a distância de um objeto ou pessoa', 4.50,  -0.45, '-X', 1);

INSERT INTO 
Dispositivo (CodigoDispositivo, IdTipo, IdAmbiente, Nome, Descricao, Eixo_X, Eixo_Y, Orientacao, Ind_Sit)
VALUES ('UIR-72', 2, 7, 'Ultrassônico',  'Usado para detectar a distância de um objeto ou pessoa', 4.50,  -1.10, '-X', 1);

INSERT INTO 
Dispositivo (CodigoDispositivo, IdTipo, IdAmbiente, Nome, Descricao, Eixo_X, Eixo_Y, Orientacao, Ind_Sit)
VALUES ('UIR-73', 2, 7, 'Ultrassônico',  'Usado para detectar a distância de um objeto ou pessoa', 3.65,  -2.10, '+X', 1);

CREATE TABLE Ambiente 
(
  IdAmbiente INT NOT NULL ,  
  Nome VARCHAR(40) NOT NULL ,
  Descricao VARCHAR(200) NULL ,
  Ind_Sit INT ,
  PRIMARY KEY (IdAmbiente)
);

INSERT INTO 
 Ambiente (IdAmbiente, Nome, Descricao, Ind_Sit)
 VALUES (1, 'Quarto 01', '', 1);

INSERT INTO 
 Ambiente (IdAmbiente, Nome, Descricao, Ind_Sit)
 VALUES (2, 'Quarto 02', '', 1);

INSERT INTO 
 Ambiente (IdAmbiente, Nome, Descricao, Ind_Sit)
 VALUES (3, 'Quarto 03', '', 1);

INSERT INTO 
 Ambiente (IdAmbiente, Nome, Descricao, Ind_Sit)
 VALUES (4, 'Sala', '', 1);

INSERT INTO 
 Ambiente (IdAmbiente, Nome, Descricao, Ind_Sit)
 VALUES (5, 'Circula��o', '', 1);

INSERT INTO 
 Ambiente (IdAmbiente, Nome, Descricao, Ind_Sit)
 VALUES (6, 'Cozinha', '', 1);

INSERT INTO 
 Ambiente (IdAmbiente, Nome, Descricao, Ind_Sit)
 VALUES (7, 'Banheiro', '', 1);

CREATE TABLE Medicao 
(
  IdMedicao SERIAL PRIMARY KEY ,
  IdDispositivo INT NULL ,
  DataHora TIMESTAMP NULL ,
  Valor VARCHAR(10) NULL ,
  Unidade CHAR(4) NULL ,
  Ind_Sit INT ,
  FOREIGN KEY (IdDispositivo) REFERENCES Dispositivo(IdDispositivo)
);
 