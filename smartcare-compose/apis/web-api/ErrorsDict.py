class Get():
    
    def ByCode(int):

        Errors = {}
        #TRATAMENTO DE VARIAVEIS
        Errors[101] = "A variável buscada foi passada mais de uma vez!"
        Errors[102] = "A variável buscada não foi passada!"
        Errors[103] = "Erro ao tratar as variáveis da requisição!"
        Errors[104] = "O valor buscado deve ser diferente de vazio!"
        Errors[105] = "Não foram passados parâmetros!"
        Errors[106] = "Nenhuma coluna foi passada para a atualização!"
        Errors[107] = "O id passado não pôde ser resolvido, ele deve ser um inteiro!"
        Errors[108] = "Rota não encontrada!"
        Errors[109] = "O valor buscado não é um inteiro!"
        Errors[110] = "As variáveis esperadas não foram passadas ou estão incorretas!"
        Errors[111] = "Erro extrair valores das variáveis do formulário!"
        Errors[112] = "Variáveis obrigatórias não foram passadas!"
        Errors[113] = "Os tipos das variáveis obrigatórias estão incorretos!"
        Errors[114] = "Erro ao decodificar as variáveis!"
        Errors[115] = "O tipo da variável está incorreto!"
        #VARIAVEIS DE AMBIENTE
        Errors[201] = "Não foi possivel resolver os dados de conexão da base de dados!"
        Errors[202] = "Erro interno na api - Tradução de dados de conexão da base de dados!"
        #CONEXÃO BASE DE DADOS
        Errors[300] = "Erro na conexão com o banco de dados, contate o suporte!"
        Errors[301] = "Erro ao se conectar à base de dados!"
        Errors[302] = "Erro interno na Api - Conexão na Base de Dados!"
        Errors[311] = "Erro ao autenticar a conexão com o banco de dados, contate o suporte!"
        #TIPO DISPOSITIVO
        Errors[401] = "Erro na listagem de tipo de dispositivo!"
        Errors[411] = "Erro na busca de tipos!"
        Errors[412] = "Erro interno na Api - busca tipo por id!"
        Errors[421] = "Erro interno na Api - busca tipo por nome!"
        Errors[431] = "A inserção foi bem sucedida, porém não encontramos os dados do tipo no banco!"
        Errors[432] = "Erro na inserção do tipo!"
        Errors[433] = "Erro interno na Api - inserir tipo!"
        Errors[441] = "A atualização do tipo foi bem sucedida, porém não encontramos os dados do tipo no banco!"
        Errors[442] = "Erro na atualização do tipo!"
        Errors[443] = "O id do tipo de dispositivo não foi localizado!"
        Errors[444] = "Erro interno na Api - atualizar tipo!"
        Errors[451] = "O nome do tipo a ser alterado não foi passado ou está incorreto!"
        Errors[452] = "Erro interno na Api - Atualizar nome do tipo!"
        Errors[461] = "A exclusão do tipo não foi bem sucedida!"
        Errors[462] = "A exclusão foi bem sucedida, mas ocorreu um erro ao buscar os índices do tipo!"
        Errors[463] = "Erro na exclusão do tipo!"
        Errors[464] = "Tipo já excluído!"
        Errors[465] = "Erro interno na Api - excluir tipo!"
        #500 - DISPOSITIVO
        Errors[501] = "Erro na listagem de dispositivo!"
        Errors[511] = "Erro interno na Api - busca dispositivo por id!"
        Errors[521] = "Erro na busca de dispositivo!"
        Errors[522] = "Erro interno na Api - busca dispositivo por texto!"
        Errors[531] = "A inserção foi bem sucedida, porém não encontramos os dados do dispositivo no banco!"
        Errors[532] = "Erro na inserção dos dispositivo!"
        Errors[533] = "Erro interno na Api - inserir dispositivo!"
        Errors[541] = "A atualização foi bem sucedida, porém não encontramos os dados do dispositivo no banco!"
        Errors[542] = "Erro na atualização do dispositivo!"
        Errors[543] = "O id do dispositivo não foi localizado!"
        Errors[544] = "Erro interno na Api - atualizar dispositivo!"
        Errors[551] = "O nome do dispositivo a ser alterado não foi passado ou está incorreto!"
        Errors[552] = "Erro interno na Api - Atualizar nome do dispositivo!"
        Errors[561] = "O codigo do dispositivo a ser alterado não foi passado ou está incorreto!"
        Errors[562] = "Erro interno na Api - Atualizar codigo do dispositivo!"
        Errors[571] = "A exclusão do dispositivo não foi bem sucedida!"
        Errors[572] = "A exclusão foi bem sucedida, mas ocorreu um erro ao buscar os índices do dispositivo!"
        Errors[573] = "Erro na exclusão do dispositivo!"
        Errors[574] = "Dispositivo já excluído!"
        Errors[575] = "Erro interno na Api - excluir dispositivo!"
        #600 - AMBIENTE
        Errors[601] = "Erro na listagem de ambiente!"
        Errors[611] = "Erro na busca de ambiente!"
        Errors[612] = "Erro interno na Api - busca ambiente por id!"
        Errors[621] = "Erro interno na Api - busca ambiente por texto!"
        Errors[631] = "A inserção foi bem sucedida, porém não encontramos os dados do ambiente no banco!"
        Errors[632] = "Erro na inserção dos ambiente!"
        Errors[633] = "Erro interno na Api - inserir ambiente!"
        Errors[641] = "A atualização foi bem sucedida, porém não encontramos os dados do ambiente no banco!"
        Errors[642] = "Erro na atualização do ambiente!"
        Errors[644] = "O id do ambiente não foi localizado!"
        Errors[645] = "Erro interno na Api - atualizar ambiente!"
        Errors[651] = "O nome do ambiente a ser alterado não foi passado ou está incorreto!"
        Errors[652] = "Erro interno na Api - Atualizar nome do ambiente!"
        Errors[661] = "Erro ao atualizar a descrição do ambiente!"
        Errors[662] = "A descrição do ambiente a ser alterado não foi passado ou está incorreto!"
        Errors[663] = "Erro interno na Api - Atualizar descrição do ambiente!"
        Errors[671] = "A exclusão do ambiente não foi bem sucedida!"
        Errors[672] = "A exclusão foi bem sucedida, mas ocorreu um erro ao buscar os índices do ambiente!"
        Errors[673] = "Erro na exclusão do ambiente!"
        Errors[674] = "Ambiente já excluído!"
        Errors[675] = "Erro interno na Api - excluir ambiente!"
        #700 - MEDICAO
        Errors[701] = "As datas passadas estão num formato inválido!"
        Errors[702] = "Erro ao Buscar medições!"
        #800 - USUARIO
        Errors[801] = "Login não encontrado!"
        Errors[802] = "Erro ao efetuar Login!"
        Errors[803] = "Erro ao tratar Login e Senha!"
        Errors[811] = "A inserção foi bem sucedida, porém não encontramos os dados do usuário no banco!"
        Errors[812] = "Erro na inserção do usuário!"
        Errors[813] = "Senha inválida! Ela deve ter mais de 6 dígitos e deve conferir com a confirmação!"
        Errors[814] = "Erro interno na Api - inserir usuário!"
        #900 - ESTADO
        Errors[901] = "Erro na listagem de estados!"
        Errors[911] = "Erro interno na Api - busca estado por id!"
        Errors[921] = "Erro na busca de estado!"
        Errors[922] = "Erro interno na Api - busca estado por texto!"
        #950 - CIDADE
        Errors[951] = "Erro na listagem de cidades!"        
        Errors[961] = "Erro interno na Api - busca cidade por id!"
        Errors[962] = "Erro interno na Api - busca cidade por id de estado!"
        Errors[971] = "Erro na busca de cidade!"
        Errors[972] = "Erro interno na Api - busca cidade por texto!"

        error = Errors[int] if int in Errors.keys() else None

        if error != None:

            return error

        else:

            return f"Ocorreu um erro, entre em contato com o suporte! (error code {int})"
