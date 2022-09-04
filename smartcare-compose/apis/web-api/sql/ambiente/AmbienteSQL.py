from pypika import Column, Criterion, Database, Dialects, Field, functions as fn, Order, queries, Query, Schema, Table
import sql.ambiente.Constants as Constants

class Consts:

    #Databases
    DB_SMARTCARE = Constants.DataBases.SMARTCARE
    #Schemas
    SC_PUBLIC = Constants.Schemas.PUBLIC
    #Tabelas    
    TB_AMBIENTE = Constants.Tables.AMBIENTE
    TB_AMBIENTE_NA = Constants.Tables.NoAlias.AMBIENTE
    #Colunas
    CL_AMBIENTE_IDAMBIENTE = Constants.Columns.Ambiente.IDAMBIENTE
    CL_AMBIENTE_IDAMBIENTE_NA = Constants.Columns.Ambiente.NoAlias.IDAMBIENTE
    CL_AMBIENTE_NOME = Constants.Columns.Ambiente.NOME
    CL_AMBIENTE_NOME_NA = Constants.Columns.Ambiente.NoAlias.NOME
    CL_AMBIENTE_DESCRICAO = Constants.Columns.Ambiente.DESCRICAO
    CL_AMBIENTE_DESCRICAO_NA = Constants.Columns.Ambiente.NoAlias.DESCRICAO
    CL_AMBIENTE_IND_SIT = Constants.Columns.Ambiente.IND_SIT
    CL_AMBIENTE_IND_SIT_NA = Constants.Columns.Ambiente.NoAlias.IND_SIT
    #Situacao
    SIT_ATIVO = Constants.Situacao.ATIVO
    SIT_INATIVO = Constants.Situacao.INATIVO
    SIT_PENDENTE = Constants.Situacao.PENDENTE
    #Listas Auxiliares
    ORDERNATIONS = [Order.asc, Order.desc]

class Get:

    def All(order: Order = Order.asc):

        table = Consts.TB_AMBIENTE
        selectColumns = table.star
        ordernationColumn = Consts.CL_AMBIENTE_IDAMBIENTE
        ordernation = order

        query = Query\
                .from_(table)\
                .select(selectColumns)\
                .orderby(ordernationColumn, order=ordernation)\
                .get_sql()

        return query

    def Actives(order: Order = Order.asc):

        table = Consts.TB_AMBIENTE
        selectColumns = table.star
        whereColumn = Consts.CL_AMBIENTE_IND_SIT
        whereCondition = Consts.SIT_ATIVO
        ordernationColumn = Consts.CL_AMBIENTE_IDAMBIENTE
        ordernation = order

        query = Query\
                .from_(table)\
                .select(selectColumns)\
                .where(whereColumn == whereCondition)\
                .orderby(ordernationColumn, order=ordernation)\
                .get_sql()
                
        return query

    class By:

        def Id(id, order: Order = Order.asc):

            table = Consts.TB_AMBIENTE
            selectColumns = table.star
            whereColumn = Consts.CL_AMBIENTE_IDAMBIENTE
            whereCondition = id
            ordernationColumn = Consts.CL_AMBIENTE_IDAMBIENTE
            ordernation = order

            query = Query\
                    .from_(table)\
                    .select(selectColumns)\
                    .where(whereColumn == whereCondition)\
                    .orderby(ordernationColumn, order=ordernation)\
                    .get_sql()
            
            return query

        def Name(string, order: Order = Order.asc):

            string = '%' + string + '%'
            table = Consts.TB_AMBIENTE
            selectColumns = table.star
            whereColumn = Consts.CL_AMBIENTE_NOME
            whereCondition = string
            ordernationColumn = Consts.CL_AMBIENTE_IDAMBIENTE
            ordernation = order

            query = Query\
                    .from_(table)\
                    .select(selectColumns)\
                    .where(fn.Upper(whereColumn).like(fn.Upper(whereCondition)))\
                    .orderby(ordernationColumn, order=ordernation)\
                    .get_sql()
            
            return query

        def Description(string, order: Order = Order.asc):

            string = '%' + string + '%'
            table = Consts.TB_AMBIENTE
            selectColumns = table.star
            whereColumn = Consts.CL_AMBIENTE_DESCRICAO
            whereCondition = string
            ordernationColumn = Consts.CL_AMBIENTE_IDAMBIENTE
            ordernation = order

            query = Query\
                    .from_(table)\
                    .select(selectColumns)\
                    .where(fn.Upper(whereColumn).like(fn.Upper(whereCondition)))\
                    .orderby(ordernationColumn, order=ordernation)\
                    .get_sql()
            
            return query

class Do:

    class Returning_():

        def All(query):

            return query + ' RETURNING *'

    def Insert(name, description = ''):

        table = Consts.TB_AMBIENTE_NA
        clName = Consts.CL_AMBIENTE_NOME_NA
        clDescription = Consts.CL_AMBIENTE_DESCRICAO_NA
        clSituation = Consts.CL_AMBIENTE_IND_SIT_NA
        situation = Consts.SIT_ATIVO

        query = Query\
                .into(table)\
                .columns(clName, clDescription, clSituation)\
                .insert(name, description, situation)\
                .get_sql()

        query = Do.Returning_.All(query)
        
        return  query     

    def Update(id, name, description):

        table = Consts.TB_AMBIENTE_NA
        clName = Consts.CL_AMBIENTE_NOME_NA
        clDescription = Consts.CL_AMBIENTE_DESCRICAO_NA
        whereColumn = Consts.CL_AMBIENTE_IDAMBIENTE_NA
        whereCondition = id
        empty = ['', None]
        name = clName if name in empty else name
        description = clDescription if description in empty else description

        query = Query\
                .update(table)\
                .set(clName, name)\
                .set(clDescription, description)\
                .where(whereColumn == whereCondition)\
                .get_sql()

        query = Do.Returning_.All(query)

        return query

    def Delete(id):

        table = Consts.TB_AMBIENTE_NA
        clInd_sit = Consts.CL_AMBIENTE_IND_SIT_NA
        sitInativo = Consts.SIT_INATIVO
        whereColumn = Consts.CL_AMBIENTE_IDAMBIENTE_NA
        whereCondition = id
        
        query = Query\
                .update(table)\
                .set(clInd_sit, sitInativo)\
                .where(whereColumn == whereCondition)\
                .get_sql()

        return query

    def VerifyExclusion(id):

        table = Consts.TB_AMBIENTE_NA
        clInd_sit = Consts.CL_AMBIENTE_IND_SIT_NA
        sitInativo = Consts.SIT_INATIVO
        whereColumn = Consts.CL_AMBIENTE_IDAMBIENTE_NA
        whereCondition = id

        query = Query\
                .from_(table)\
                .select(whereColumn)\
                .where(whereColumn == whereCondition)\
                .where(clInd_sit != sitInativo)\
                .get_sql()

        return query

    class UpdateColumn:

        def Name(id, name):

            table = Consts.TB_AMBIENTE_NA
            clName = Consts.CL_AMBIENTE_NOME_NA
            whereColumn = Consts.CL_AMBIENTE_IDAMBIENTE_NA
            whereCondition = id
            empty = ['', None]
            name = clName if name in empty else name

            query = Query\
                    .update(table)\
                    .set(clName, name)\
                    .where(whereColumn == whereCondition)\
                    .get_sql()

            query = Do.Returning_.All(query)

            return query

        def Description(id, description):

            table = Consts.TB_AMBIENTE_NA
            clDescription = Consts.CL_AMBIENTE_DESCRICAO_NA
            whereColumn = Consts.CL_AMBIENTE_IDAMBIENTE_NA
            whereCondition = id
            empty = ['', None]
            description = clDescription if description in empty else description

            query = Query\
                    .update(table)\
                    .set(clDescription, description)\
                    .where(whereColumn == whereCondition)\
                    .get_sql()

            query = Do.Returning_.All(query)

            return query
