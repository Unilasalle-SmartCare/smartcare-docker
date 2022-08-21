from pypika import Column, Database, Dialects, Schema, Table

#Database
class DataBases:

    SMARTCARE = Database('smartcare')

#Schemas
class Schemas:

    PUBLIC = Schema('public')

#Tabelas
class Tables:

    AMBIENTE = Table('ambiente', schema=Schemas.PUBLIC, alias="amb")

    class NoAlias:

        AMBIENTE = Table('ambiente', schema=Schemas.PUBLIC)

#Colunas
class Columns:

    class Ambiente:

        IDAMBIENTE = Tables.AMBIENTE.idambiente
        NOME = Tables.AMBIENTE.nome
        DESCRICAO = Tables.AMBIENTE.descricao
        IND_SIT = Tables.AMBIENTE.ind_sit

        class NoAlias:
            
            IDAMBIENTE = Tables.NoAlias.AMBIENTE.idambiente
            NOME = Tables.NoAlias.AMBIENTE.nome
            DESCRICAO = Tables.NoAlias.AMBIENTE.descricao
            IND_SIT = Tables.NoAlias.AMBIENTE.ind_sit

#Situacao
class Situacao:

    ATIVO = 1
    INATIVO = 2
    PENDENTE = 3