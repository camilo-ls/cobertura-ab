
# Cálculo da cobertura:
# Cobertura = ((nºeSF*3450 + (nºeAP + nºeSFseq)*3000)/estim. pop)*100
# nºeSF: eSFs com código 70 nos estabelecimentos válidos
# nºeAB: eABs com código 76 nos estabelecimentos válidos
# nºeSFeq: equivalentes nos estabelecimentos válidos

# Importação de bibliotecas:
import pandas as pd 
import os
import math
from unidecode import unidecode

''' =================================================================================== 
    Caminho/relação das bases utilizadas
    =================================================================================== '''

# Caminhos da raiz (onde este arquivo está):
rootPath = os.path.dirname(os.path.abspath(__file__))
## Bancos municipais:
rawEstMun = rootPath + '/TXTPROC_130260/lfces004.txt'
rawEquipesMun = rootPath + '/TXTPROC_130260/lfces037.txt'
rawProfsMun = rootPath + '/TXTPROC_130260/lfces038.txt'
rawProfsMunRH = rootPath + '/TXTPROC_130260/lfces018.txt'
rawCHMun = rootPath + '/TXTPROC_130260/lfces021.txt'
rawInconfMun = rootPath + '/TXTPROC_130260/nfces071.txt'

## Bancos estaduais:
rawEst = rootPath + '/TXTPROC_13/lfces004.txt'
rawEquipes = rootPath + '/TXTPROC_13/lfces037.txt'
rawProfs = rootPath + '/TXTPROC_13/lfces018.txt'
rawProfsEquipes = rootPath + '/TXTPROC_13/lfces038.txt'
rawCH = rootPath + '/TXTPROC_13/lfces021.txt'
rawInconf = rootPath + '/TXTPROC_13/nfces071.txt'

## Demais informações
rawCnes = rootPath + '/cnes.xlsx'
rawPop = rootPath + '/pop.xlsx'

''' =================================================================================== 
    Bases municipais # Carregando as bases para a memória (dataframes) / Formatação
    =================================================================================== '''

# Carregando a relação de Cnes e População:
dfCnes = pd.read_excel(rawCnes)
dfPop = pd.read_excel(rawPop)

# Estruturação do dataframe
# >> Informação adquirida no Caderno Layout de TXT SCNES <<
# Montagem do cabeçalho:
# -> headerCols: nomes das colunas
# -> headerWidth: largura das colunas
headerCols = ['UNIDADE_ID', 'CNES', 'CNPJ_MANT', 'PFPJ_IND', 'R_SOCIAL', 'NOME_FONT', 'CPF', 'CNPJ', 'TP_UNID_ID', 'SIGESTGEST', 'CODMUNGEST', 'CO_NATUREZA_JUR', 'DATA_ATU', 'USUARIO', 'REG_SAUDE', 'CHECKSUM']
headerWidth = [31, 7, 14, 1, 60, 60, 11, 14, 2, 2, 7, 4, 10, 12, 4, 24]
# carrega o dataframe:
dfEstabMun = pd.read_fwf(rawEstMun, widths=headerWidth, header=None, names=headerCols, skiprows=1) # skiprow: pula a primeira linha (é um cód. de identificação)

# Repete os processos para os demais bancos:
# Equipes:
headerCols = ['COD_MUN', 'COD_AREA', 'SEQ_EQUIPE', 'UNIDADE_ID', 'TP_EQUIPE', 'NM_REFERENCIA', 'DT_ATIVACAO', 'DT_DESATIVACAO', 'CD_MOTIVO_DESATIV', 'CD_TP_DESATIV', 'STATUSMOV', 'DATA_ATU', 'USUARIO', 'CO_PROF_SUS_PRECEPTOR', 'CO_CNES_PRECEPTOR', 'CO_EQUIPE', 'CHECKSUM']
headerWidth = [6, 4, 8, 31, 2, 60, 10, 10, 2, 2, 1, 10, 12, 16, 7, 10, 24]
dfEquipesMun = pd.read_fwf(rawEquipesMun, widths=headerWidth, header=None, names=headerCols, skiprows=1)

# Profissionais das equipes:
headerCols = ['COD_MUN', 'COD_AREA', 'SEQ_EQUIPE', 'PROF_ID', 'UNIDADE_ID', 'COD_CBO', 'IND_VINC', 'TP_SUS_NAO_SUS', 'FL_EQUIPEMINIMA', 'MICROAREA', 'DT_ENTRADA', 'DT_DESLIGAMENTO', 'DATA_ATU', 'USUARIO', 'CO_EQUIPE', 'CHECKSUM']
headerWidth = [6, 4, 8, 16, 31, 6, 6, 1, 1, 2, 10, 10, 10, 12, 10, 24]
dfProfsMun = pd.read_fwf(rawProfsMun, widths=headerWidth, header=None, names=headerCols, skiprows=1, dtype={'PROF_ID': str})

# Informações dos profissionais
headerCols = ['PROF_ID', 'CPF_PROF', 'NOME_PROF', 'COD_CNS', 'DATA_ATU', 'USUARIO', 'CHECKSUM']
headerWidth = [16, 11, 60, 15, 10, 12, 24]
dfProfsRHMun = pd.read_fwf(rawProfsMunRH, widths=headerWidth, header=None, names=headerCols, skiprows=1, dtype={'PROF_ID': str, 'CPF_PROF': str})
## filtra as informações necessárias:
dfProfsRHMun = dfProfsRHMun[['PROF_ID', 'CPF_PROF', 'NOME_PROF']]

# CH dos profissionais:
headerCols = ['UNIDADE_ID', 'PROF_ID', 'COD_CBO', 'brancos1', 'IND_VINC', 'CGHORAOUTR', 'CG_HORAAMB', 'brancos2', 'CONSELHOID', 'N_REGISTRO', 'STATUS', 'STATUSMOV', 'USUARIO', 'DATA_ATU', 'COD_CNS', 'TP_PRECEPTOR', 'TP_RESIDENTE', 'CGHORAHOSP', 'CHECKSUM']
headerWidth = [31, 16, 6, 1, 6, 3, 3, 10, 2, 13, 1, 1, 12, 10, 15, 1, 1, 3, 24]
dfCHMun = pd.read_fwf(rawCHMun, widths=headerWidth, header=None, names=headerCols, skiprows=1, dtype={'PROF_ID': str})

# Profissionais com inconformidades
headerCols = ['CNES', 'CPF_PROF', 'COD_CNS', 'FL_ART_PORTARIA', 'CHECKSUM']
headerWidth = [7, 11, 15, 1, 24]
dfInconfMun = pd.read_fwf(rawInconfMun, widths=headerWidth, header=None, names=headerCols, skiprows=1, dtype={'CPF_PROF': str})
## filtra somente as informações necessárias:
dfInconfMun = dfInconfMun[['CPF_PROF']]
listaInvalidos = dfInconfMun['CPF_PROF'].values.tolist()

# Criação de uma lista para saber se determinado profissional já foi contabilizado:
listaProfsContabilizados = []

# Dicionário que faz a relação do número de equipes para cada bairro
## O formato é: {LOCALIDADE: [NUM_ESF, NUM_EAB, NUM_ESQeq]}
listaEquipesLocalidade = {}

''' =================================================================================== 
    Bases municipais # Filtrando os dataframes
    =================================================================================== '''

# Seleciona somente as colunas necessárias:
dfCnes = dfCnes[['CNES', 'BAIRRO', 'DISTRITO']]
dfPop.columns = ['BAIRRO', 'POP']

# Trata os valores dos na tabela de população e do CNES, a fim de fazer uma correspondência de valor entre as tabelas:
## Coloca os caracteres em maiúsculo e retira os acentos:
dfPop['BAIRRO'] = dfPop['BAIRRO'].str.upper().apply(unidecode)
dfCnes['BAIRRO'] = dfCnes['BAIRRO'].str.upper().apply(unidecode)
## Faz o join entre as tabelas:
dfCnes = dfCnes.merge(dfPop, on=['BAIRRO'], how='left')

# Filtra os estabelecimentos por tipo:
## Tipos: 01, 02, 32, 40
tipos = [1, 2, 32, 40]
dfEstabMun = dfEstabMun[dfEstabMun['TP_UNID_ID'].isin(tipos)]
# Faz o filtro dos dos estabelecimentos municipais pela Natureza Jurídica (fonte: nota metodológica adaptada)
# * Códigos válidos:
# 1000, 1015, 1023, 1031, 1040, 1058, 1066, 1074, 1082, 1104, 1112, 1120, 1139, 1147, 1155, 1163, 1171, 1180, 1198, 1201, 1210, 1228, 1236, 1244, 1252, 1260, 1279
natJur = [100, 1015, 1023, 1031, 1040, 1058, 1066, 1074, 1082, 1104, 1112, 1120, 1139, 1147, 1155, 1163, 1171, 1180, 1198, 1201, 1210, 1228, 1236, 1244, 1252, 1260, 1279]
dfEstabMun = dfEstabMun[dfEstabMun['CO_NATUREZA_JUR'].isin(natJur)]
## Filtra os estabelecimentos que não são da SEMSA:
dfEstabMun = dfEstabMun[dfEstabMun['R_SOCIAL'] == 'MANAUS SECRETARIA MUNICIPAL DE SAUDE']
# Cria a relação dos IDS das unidades filtradas:
listaIdUnidades = dfEstabMun['UNIDADE_ID'].values.tolist()

# Elimina as equipes que não estão na relação de Estabelecimentos filtrados anteriormente:
dfEquipesMun = dfEquipesMun[dfEquipesMun['UNIDADE_ID'].isin(listaIdUnidades)]
# Elimina as equipes que possuem data de desativação ()
dfEquipesMun = dfEquipesMun[dfEquipesMun['DT_DESATIVACAO'].isnull()]
# Cria a relação das equipes filtradas:
listaEquipes = dfEquipesMun['CO_EQUIPE'].values.tolist()

# Filtra os profissionais que não estão nos estabelecimentos filtrados:
dfProfsMun = dfProfsMun[dfProfsMun['UNIDADE_ID'].isin(listaIdUnidades)]
# Filtra os profissionais que não estão nas equipes filtradas:
dfProfsMun = dfProfsMun[dfProfsMun['CO_EQUIPE'].isin(listaEquipes)]
# Filtra os profissionais que possuem data de desligamento:
dfProfsMun = dfProfsMun[dfProfsMun['DT_DESLIGAMENTO'].isnull()]
# Retira os profissionais que não possuem um dos CBOs de interesse:
## OBS: A conversão para string é necessária para que se possa 'fatiar' os primeiros 4 dígitos da string, isso porque os CBOs tem 6 dígitos no total
dfProfsMun = dfProfsMun[dfProfsMun['COD_CBO'].str[0:4].isin(['2251', '2231', '2252', '2253', '2235', '3222', '5151'])]

# Retira do dataframe de CH todas as colunas que não nos interessam:
dfCHMun = dfCHMun[['UNIDADE_ID', 'PROF_ID', 'COD_CBO', 'CGHORAOUTR', 'CG_HORAAMB', 'CGHORAHOSP']]

# Faz o join do dfProfsMun com o dfCHMun, utilizando PROF_ID, UNIDADE_ID e COD_CBO como vínculos entre os DFs, para que o dfProfsMun agora tenha as colunas de carga horária:
#print(dfProfsMun.shape[0])
dfProfsMun = dfProfsMun.merge(dfCHMun, on=['PROF_ID', 'UNIDADE_ID', 'COD_CBO'], how='left')
#print(dfProfsMun.shape[0])
dfProfsMun = dfProfsMun.merge(dfProfsRHMun, on=['PROF_ID'], how='left')
#print(dfProfsMun.shape[0])
# Faz o 'merge' dos duplicados, somando as respectivas cargas horárias:
dfProfsMun = dfProfsMun.groupby(['PROF_ID', 'CPF_PROF', 'NOME_PROF', 'UNIDADE_ID', 'COD_CBO', 'CO_EQUIPE'], as_index=False).agg({'CGHORAOUTR': 'sum', 'CG_HORAAMB': 'sum', 'CGHORAHOSP': 'sum'})

''' =================================================================================== 
    Loop para cálculo de cada bairro/Filtro por CNES
    =================================================================================== '''

# A ideia é fazer um loop que segue a seguinte lógica:
# 1. Fazer uma iteração bairro por bairro, precisando, para isso:
# 2. Filtrar os CNES que pertencem a determinado bairro, e:
# 3. Aplicar esse filtro aos estabelecimentos válidos.
# 
# Assim, por consequência, como o df de estabelecimentos é o 'filtro maior', a partir do qual
# também são filtrados os profissionais, se esses estabelecimentos forem filtrados por bairro,
# todo o resto também o será.

print(dfCnes.head(100))

dfCobertura = pd.DataFrame(columns=['BAIRRO', 'ESFs', 'EAPs', 'ESFsEq', 'COBERTURA'])

dfBairros = dfCnes['BAIRRO'].unique()
for bairro in dfBairros:
    if (bairro == 'DISTRITO LESTE'):
        pop = 542593
        listaProfsContabilizados = []
        dfBairro = dfCnes[dfCnes['DISTRITO'] == 'LESTE']
    elif (bairro == 'DISTRITO NORTE'):
        pop = 653723
        listaProfsContabilizados = []
        dfBairro = dfCnes[dfCnes['DISTRITO'] == 'NORTE']
    elif (bairro == 'DISTRITO OESTE'):
        pop = 494004
        listaProfsContabilizados = []
        dfBairro = dfCnes[dfCnes['DISTRITO'] == 'OESTE']
    elif (bairro == 'DISTRITO RURAL'):
        pop = 14598
        listaProfsContabilizados = []
        dfBairro = dfCnes[dfCnes['DISTRITO'] == 'RURAL']
    elif (bairro == 'DISTRITO SUL'):
        pop = 477845
        listaProfsContabilizados = []
        dfBairro = dfCnes[dfCnes['DISTRITO'] == 'SUL']
    elif (bairro == 'MANAUS'):
        pop = 2182763
        listaProfsContabilizados = []
    else:
        dfBairro = dfCnes[dfCnes['BAIRRO'] == bairro]
        pop = round(dfBairro['POP'].max()) 
    listaCnes = dfBairro['CNES'].values.tolist()
    listaUnidadesBairro = dfEstabMun[dfEstabMun['CNES'].isin(listaCnes)]['UNIDADE_ID'].values.tolist()    
    
    print('==============================================================================')
    print('BAIRRO:', bairro)
    print('Unidades:', listaUnidadesBairro)
    print('pop:', pop)
    print('')

    ''' =================================================================================== 
        Cálculo das eSFs
        =================================================================================== '''

    # CÁLCULO DAS ESF
    ## NUM_MED: 2251, 2231, 2252, 2253
    ## NUM_ENF: 2235
    ## NUM_TEC: 3222
    ## NUM_ACS: 5151
    ## CH: >= 32h
    
    # Filtra somente as Equipes de tipo 70 (eSFs):
    dfEquipes70 = dfEquipesMun[dfEquipesMun['TP_EQUIPE'] == 70]
    # Filtra as equipes que estão no bairro:
    if (bairro != 'MANAUS'): dfEquipes70 = dfEquipes70[dfEquipes70['UNIDADE_ID'].isin(listaUnidadesBairro)]    
    
    # Contador de esfs:
    nEsfs = 0
    # Para cada equipe:
    for idx, row in dfEquipes70.iterrows():
        # Inicia uma lista onde os índices correspondem a quantidade de profissionais válidos daquela equipe:
        ## idx 0: médicos
        ## idx 1: enfermeiros
        ## idx 2: t. enfermagem
        ## idx 3: acs
        rhEquipe = [0, 0, 0, 0]
        # Pega os profissionais dessa equipe:
        profissionais = dfProfsMun[dfProfsMun['CO_EQUIPE'] == row['CO_EQUIPE']]
        # Para cada profissioanal da equipe:
        for idxProf, profissional in profissionais.iterrows():
            # Cria uma chave para contabilizá-lo (e evitar repetições depois):
            chaveContabilizado = str(profissional['PROF_ID']) + '-' + str(profissional['UNIDADE_ID'])
            # Elimina o profissional já contabilizado ou inválido:
            if profissional['CPF_PROF'] in listaInvalidos or chaveContabilizado in listaProfsContabilizados:
                continue
            # Calcula a CH:
            chProf = profissional['CG_HORAAMB'] + profissional['CGHORAOUTR']
            chAmb = profissional['CG_HORAAMB']
            chHosp = profissional['CGHORAHOSP']
            chOutros = profissional['CGHORAOUTR']
            chTotal = chAmb + chHosp + chOutros
            if chAmb > 60: continue
            if chHosp > 96: continue
            if chOutros > 44: continue
            if chTotal > 120: continue
            # Se for pelo menos 32h:
            if chProf >= 32:                
                # Verifica se o profissional é médico e contabiliza se o for:
                if str(profissional['COD_CBO'])[0:4] in ('2251', '2231', '2252', '2253'):
                    rhEquipe[0] += 1
                    listaProfsContabilizados.append(chaveContabilizado)
                # Verifica se é enfermeiro:
                if str(profissional['COD_CBO'])[0:4] in ('2235'):
                    rhEquipe[1] += 1
                    listaProfsContabilizados.append(chaveContabilizado)
                # Verifica se é técnico:
                if str(profissional['COD_CBO'])[0:4] in ('3222'):
                    rhEquipe[2] += 1
                    listaProfsContabilizados.append(chaveContabilizado)
                # Verifica se é ACS:
                if str(profissional['COD_CBO'])[0:4] in ('5151'):
                    rhEquipe[3] += 1
                    listaProfsContabilizados.append(chaveContabilizado)
        # Verifica se a equipe é válida (pelo menos 1 profissional de cada categoria) e contabiliza:
        if rhEquipe[0] >= 1 and rhEquipe[1] >= 1 and rhEquipe[2] >= 1 and rhEquipe[3] >= 1:
                nEsfs += 1

    print('> eSFs:', nEsfs)

    ''' =================================================================================== 
        Cálculo das eEAPs
        =================================================================================== '''

    #print('\n> Calculando as eAPs...')

    # CÁLCULO DAS EAPS
    ## inicia um dicionário para cada equipe, que será no formato: {'CO_EQUIPE': [NUM_MED, NUM_ENF, NUM_TEC, NUM_ACS]}, onde serão considerados os cbos:
    ## NUM_MED: 225125, 225130, 225142, 225170
    ## NUM_ENF: 223505, 223565
    ## CH: >= 20h

    # Filtra somente as Equipes de tipo 76 (eAPs):
    dfEquipes76 = dfEquipesMun[dfEquipesMun['TP_EQUIPE'] == 76]
    # Filtra as equipes que estão no bairro:
    if (bairro != 'MANAUS'): dfEquipes76 = dfEquipes76[dfEquipes76['UNIDADE_ID'].isin(listaUnidadesBairro)]
    
    # Contador de esfs:
    nEaps = 0
    # Para cada equipe:
    for idx, row in dfEquipes76.iterrows():
        # Inicia uma lista onde os índices correspondem a quantidade de profissionais válidos daquela equipe:
        ## idx 0: médicos
        ## idx 1: enfermeiros
        ## idx 2: t. enfermagem
        ## idx 3: acs
        rhEquipe = [0, 0]
        # Pega os profissionais dessa equipe:
        profissionais = dfProfsMun[dfProfsMun['CO_EQUIPE'] == row['CO_EQUIPE']]
        # Para cada profissioanal da equipe:
        for idxProf, profissional in profissionais.iterrows():
            # Cria uma chave para contabilizá-lo (e evitar repetições depois):
            chaveContabilizado = str(profissional['PROF_ID']) + '-' + str(profissional['UNIDADE_ID'])
            # Elimina o profissional já contabilizado ou inválido:
            if profissional['CPF_PROF'] in listaInvalidos or chaveContabilizado in listaProfsContabilizados:
                continue
            # Calcula a CH:
            chProf = profissional['CG_HORAAMB'] + profissional['CGHORAOUTR']
            chAmb = profissional['CG_HORAAMB']
            chHosp = profissional['CGHORAHOSP']
            chOutros = profissional['CGHORAOUTR']
            chTotal = chAmb + chHosp + chOutros
            if chAmb > 60: continue
            if chHosp > 96: continue
            if chOutros > 44: continue
            if chTotal > 120: continue
            # Se for pelo menos 32h:
            if chProf >= 20:                
                # Verifica se o profissional é médico e contabiliza se o for:
                if str(profissional['COD_CBO']) in ('225125', '225130', '225142', '225170'):
                    rhEquipe[0] += 1
                    listaProfsContabilizados.append(chaveContabilizado)
                # Verifica se é enfermeiro:
                if str(profissional['COD_CBO']) in ('223505', '223565'):
                    rhEquipe[1] += 1
                    listaProfsContabilizados.append(chaveContabilizado)                
        # Verifica se a equipe é válida (pelo menos 1 profissional de cada categoria) e contabiliza:
        if rhEquipe[0] >= 1 and rhEquipe[1] >= 1:
                nEaps += 1

    print('> eAPs:', nEaps)

    ''' =================================================================================== 
        Cálculo das eSFs equivalentes
        =================================================================================== '''

    #print('\n> Calculando as eSFs equivalentes...')

    # CÁLCULO DAS ESFS EQUIVALENTES:
    ## inicia um dicionário para cada equipe, que será no formato: {'CO_EQUIPE': [NUM_MED, NUM_ENF, NUM_TEC, NUM_ACS]}, onde serão considerados os cbos:
    ## NUM_MED: 225125, 225170, 225124, 225250, 225142, 225130
    ## NUM_ENF: 2235**
    ## CH ambulatorial: >= 60h (médicos); >= 40h (enfermeiros)
    ## CH excedente não será contabilizada: 44h (outros); 60h (ambulatoriais); 96h (hospitalares); 120h (soma)

    #print('>>>> Carregando as bases para a memória...')

    # Estruturação do dataframe
    # >> Informação adquirida no Caderno Layout de TXT SCNES <<
    # Montagem do cabeçalho:
    # -> headerCols: nomes das colunas
    # -> headerWidth: largura das colunas
    headerCols = ['UNIDADE_ID', 'CNES', 'CNPJ_MANT', 'PFPJ_IND', 'R_SOCIAL', 'NOME_FONT', 'CPF', 'CNPJ', 'TP_UNID_ID', 'SIGESTGEST', 'CODMUNGEST', 'CO_NATUREZA_JUR', 'DATA_ATU', 'USUARIO', 'REG_SAUDE', 'CHECKSUM']
    headerWidth = [31, 7, 14, 1, 60, 60, 11, 14, 2, 2, 7, 4, 10, 12, 4, 24]
    # carrega o dataframe:
    dfEstab = pd.read_fwf(rawEst, widths=headerWidth, header=None, names=headerCols, skiprows=1) # skiprow: pula a primeira linha (é um cód. de identificação)

    # Repete os processos para os demais bancos:
    # Informações dos profissionais
    headerCols = ['PROF_ID', 'CPF_PROF', 'NOME_PROF', 'COD_CNS', 'DATA_ATU', 'USUARIO', 'CHECKSUM']
    headerWidth = [16, 11, 60, 15, 10, 12, 24]
    dfProfs = pd.read_fwf(rawProfs, widths=headerWidth, header=None, names=headerCols, skiprows=1, dtype={'PROF_ID': str, 'CPF_PROF': str})
    ## filtra as informações necessárias:
    dfProfs = dfProfs[['PROF_ID', 'CPF_PROF', 'NOME_PROF']]

    # CH dos profissionais:
    headerCols = ['UNIDADE_ID', 'PROF_ID', 'COD_CBO', 'brancos1', 'IND_VINC', 'CGHORAOUTR', 'CG_HORAAMB', 'brancos2', 'CONSELHOID', 'N_REGISTRO', 'STATUS', 'STATUSMOV', 'USUARIO', 'DATA_ATU', 'COD_CNS', 'TP_PRECEPTOR', 'TP_RESIDENTE', 'CGHORAHOSP', 'CHECKSUM']
    headerWidth = [31, 16, 6, 1, 6, 3, 3, 10, 2, 13, 1, 1, 12, 10, 15, 1, 1, 3, 24]
    dfCH = pd.read_fwf(rawCH, widths=headerWidth, header=None, names=headerCols, skiprows=1, dtype={'PROF_ID': str})

    # Profissionais das equipes:
    headerCols = ['COD_MUN', 'COD_AREA', 'SEQ_EQUIPE', 'PROF_ID', 'UNIDADE_ID', 'COD_CBO', 'IND_VINC', 'TP_SUS_NAO_SUS', 'FL_EQUIPEMINIMA', 'MICROAREA', 'DT_ENTRADA', 'DT_DESLIGAMENTO', 'DATA_ATU', 'USUARIO', 'CO_EQUIPE', 'CHECKSUM']
    headerWidth = [6, 4, 8, 16, 31, 6, 6, 1, 1, 2, 10, 10, 10, 12, 10, 24]
    dfProfsEquipesMun = pd.read_fwf(rawProfsMun, widths=headerWidth, header=None, names=headerCols, skiprows=1, dtype={'PROF_ID': str})

    # Informações dos profissionais do município:
    headerCols = ['PROF_ID', 'CPF_PROF', 'NOME_PROF', 'COD_CNS', 'DATA_ATU', 'USUARIO', 'CHECKSUM']
    headerWidth = [16, 11, 60, 15, 10, 12, 24]
    dfProfsMunEq = pd.read_fwf(rawProfsMunRH, widths=headerWidth, header=None, names=headerCols, skiprows=1, dtype={'PROF_ID': str, 'CPF_PROF': str})
    ## filtra as informações necessárias:
    dfProfs = dfProfs[['PROF_ID', 'CPF_PROF', 'NOME_PROF']]

    # CH dos profissionais:
    headerCols = ['UNIDADE_ID', 'PROF_ID', 'COD_CBO', 'brancos1', 'IND_VINC', 'CGHORAOUTR', 'CG_HORAAMB', 'brancos2', 'CONSELHOID', 'N_REGISTRO', 'STATUS', 'STATUSMOV', 'USUARIO', 'DATA_ATU', 'COD_CNS', 'TP_PRECEPTOR', 'TP_RESIDENTE', 'CGHORAHOSP', 'CHECKSUM']
    headerWidth = [31, 16, 6, 1, 6, 3, 3, 10, 2, 13, 1, 1, 12, 10, 15, 1, 1, 3, 24]
    dfCHMun = pd.read_fwf(rawCHMun, widths=headerWidth, header=None, names=headerCols, skiprows=1, dtype={'PROF_ID': str})

    # Profissionais com inconformidades
    headerCols = ['CNES', 'CPF_PROF', 'COD_CNS', 'FL_ART_PORTARIA', 'CHECKSUM']
    headerWidth = [7, 11, 15, 1, 24]
    dfInconf = pd.read_fwf(rawInconf, widths=headerWidth, header=None, names=headerCols, skiprows=1, dtype={'CPF_PROF': str})
    ## filtra somente as informações necessárias:
    dfInconf = dfInconf[['CPF_PROF']]
    listaInvalidos2 = dfInconf['CPF_PROF'].values.tolist()

    # Filtra os estabelecimentos por tipo:
    ## Tipos: 01, 02, 32, 40
    tipos = [1, 2, 32, 40]
    dfEstab = dfEstab[dfEstab['TP_UNID_ID'].isin(tipos)]
    # Faz o filtro dos dos estabelecimentos municipais pela Natureza Jurídica (fonte: nota metodológica adaptada)
    # * Códigos válidos:
    # 1000, 1015, 1023, 1031, 1040, 1058, 1066, 1074, 1082, 1104, 1112, 1120, 1139, 1147, 1155, 1163, 1171, 1180, 1198, 1201, 1210, 1228, 1236, 1244, 1252, 1260, 1279
    natJur = [100, 1015, 1023, 1031, 1040, 1058, 1066, 1074, 1082, 1104, 1112, 1120, 1139, 1147, 1155, 1163, 1171, 1180, 1198, 1201, 1210, 1228, 1236, 1244, 1252, 1260, 1279]
    dfEstab = dfEstab[dfEstab['CO_NATUREZA_JUR'].isin(natJur)]
    dfEstab = dfEstab[dfEstab['CODMUNGEST'] == 130260]
    # Cria a relação dos IDS das unidades filtradas:
    listaIdUnidades2 = dfEstab['UNIDADE_ID'].values.tolist()

    # Retira do dataframe de CH todas as colunas que não nos interessam:
    dfCH = dfCH[['UNIDADE_ID', 'PROF_ID', 'COD_CBO', 'CGHORAOUTR', 'CG_HORAAMB', 'CGHORAHOSP']]
    dfCHMun = dfCHMun[['UNIDADE_ID', 'PROF_ID', 'COD_CBO', 'CGHORAOUTR', 'CG_HORAAMB', 'CGHORAHOSP']]

    # Faz o join do dfProfs com o dfCH, utilizando PROF_ID, UNIDADE_ID e COD_CBO como vínculos entre os DFs, para que o dfProfs agora tenha as colunas de carga horária:
    dfProfs = dfProfs.merge(dfCH, on=['PROF_ID'], how='left')
    dfProfsMunEq = dfProfsMunEq.merge(dfCHMun, on=['PROF_ID'], how='left')

    #
    dfProfsEquipesMun = dfProfsEquipesMun[['PROF_ID']]
    listaProfsEquipes = dfProfsEquipesMun['PROF_ID'].values.tolist()

    # Filtra os profissionais que não estão nos estabelecimentos filtrados:
    dfProfs = dfProfs[dfProfs['UNIDADE_ID'].isin(listaIdUnidades2)]
    if (bairro != 'MANAUS'): dfProfs = dfProfs[dfProfs['UNIDADE_ID'].isin(listaUnidadesBairro)]
    dfProfsMunEq = dfProfsMunEq[dfProfsMunEq['UNIDADE_ID'].isin(listaIdUnidades)]
    if (bairro != 'MANAUS'): dfProfsMunEq = dfProfsMunEq[dfProfsMunEq['UNIDADE_ID'].isin(listaUnidadesBairro)]
    dfProfsMunEq = dfProfsMunEq[~dfProfsMunEq['PROF_ID'].isin(listaProfsEquipes)]  


    rhEquipes = {'MED': 0, 'ENF': 0}

    for idx, row in dfProfs.iterrows():
        chaveContabilizado = str(row['PROF_ID']) + '-' + str(row['UNIDADE_ID'])
        if row['CPF_PROF'] in listaInvalidos2 or chaveContabilizado in listaProfsContabilizados:
            continue
        # Calcula a CH:   
        chAmb = row['CG_HORAAMB']
        chHosp = row['CGHORAHOSP']
        chOutros = row['CGHORAOUTR']
        chTotal = chAmb + chHosp + chOutros
        if chAmb > 60: continue
        if chHosp > 96: continue
        if chOutros > 44: continue
        if chTotal > 120: continue
        # Verifica se o profissional é médico e contabiliza se o for:
        if str(row['COD_CBO']) in ('225125', '225170', '225124', '225250', '225142', '225130'):        
            rhEquipes['MED'] += chTotal
            listaProfsContabilizados.append(chaveContabilizado)
        # Verifica se é enfermeiro:
        if str(row['COD_CBO'])[0:4] in ('2235'):        
            rhEquipes['ENF'] += chTotal
            listaProfsContabilizados.append(chaveContabilizado)

    for idx, row in dfProfsMunEq.iterrows():
        chaveContabilizado = str(row['PROF_ID']) + '-' + str(row['UNIDADE_ID'])
        if row['CPF_PROF'] in listaInvalidos or chaveContabilizado in listaProfsContabilizados:        
            continue
        # Calcula a CH:   
        chAmb = row['CG_HORAAMB']
        chHosp = row['CGHORAHOSP']
        chOutros = row['CGHORAOUTR']
        chTotal = chAmb + chHosp + chOutros
        if chAmb > 60: continue
        if chHosp > 96: continue
        if chOutros > 44: continue
        if chTotal > 120: continue
        # Verifica se o profissional é médico e contabiliza se o for:
        if str(row['COD_CBO']) in ('225125', '225170', '225124', '225250', '225142', '225130'):        
            rhEquipes['MED'] += chTotal
            listaProfsContabilizados.append(chaveContabilizado)
        # Verifica se é enfermeiro:
        if str(row['COD_CBO'])[0:4] in ('2235'):        
            rhEquipes['ENF'] += chTotal
            listaProfsContabilizados.append(chaveContabilizado)

    # Contabiliza o número de eSFs válidas (pelo menos 1 profissional de cada categoria):
    #print('>>> Contabilizando o número de equipes...')
    rhEquipes['MED'] = rhEquipes['MED']/60
    rhEquipes['ENF'] = rhEquipes['ENF']/40

    if (rhEquipes['MED'] < rhEquipes['ENF']): nEsfeq = rhEquipes['MED']
    else: nEsfeq = rhEquipes['ENF']

    print('> EsfEq.: ', nEsfeq)
    print('')
    # Cobertura = ((nºeSF*3450 + (nºeAP + nºeSFseq)*3000)/estim. pop)*100
    cobertura = ((nEsfs*3450 + (nEaps + nEsfeq)*3000)/pop)*100
    #['BAIRRO', 'ESFs', 'EAPs', 'ESFsEq', 'COBERTURA']
    novaLinha = {'BAIRRO': bairro, 'ESFs': nEsfs, 'EAPs': nEaps, 'ESFsEq': nEsfeq, 'COBERTURA': str(cobertura) + '%'}
    dfCobertura = dfCobertura.append(novaLinha, ignore_index=True)    
    print('COBERTURA: ' + str(cobertura) + '%')

dfCobertura.to_excel(rootPath + '/cobertura.xlsx', index=False)