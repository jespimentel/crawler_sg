import sys
import os
import datetime
import hashlib
import requests
from bs4 import BeautifulSoup

def consulta_por_parte(nome_da_parte):
    """Obtém a resposta da pesquisa por parte"""

    # URL base da pesquisa
    base_url = "https://esaj.tjsp.jus.br/cposg/search.do"

    # Payload da requisição
    payload = {
        "conversationId": "",
        "paginaConsulta": "0",
        "cbPesquisa": "NMPARTE",
        "dePesquisa": nome_da_parte,
        "localPesquisa.cdLocal": "4", # Somente Direito Criminal
    }

    # Realiza a requisição e armazena o resultado na variável 'response'
    response = requests.post(base_url, data=payload)

    return response


def consulta_num_oab(numero_oab):
    # URL base da pesquisa
    base_url = "https://esaj.tjsp.jus.br/cposg/search.do"

    # Payload da requisição
    payload = {
        "conversationId": "",
        "paginaConsulta": "0",
        "cbPesquisa": "NUMOAB",
        "dePesquisa": numero_oab,
        "localPesquisa.cdLocal": "4",# Somente Direito Criminal
    }

    # Realiza a requisição e armazena o resultado na variável 'response'
    response = requests.post(base_url, data=payload)

    return response


def faz_busca(soup):
    """Analisa e retorna a resposta da consulta"""
    # Não existem processos ou muitos processos
    mensagem = soup.find('div', {'id': 'spwTabelaMensagem'})
    if mensagem is not None:
        texto = mensagem.find('td', {'id':'mensagemRetorno'})
        texto = texto.find('li').text
        return texto
    
    # Encontro de uma lista de processos
    relacao_processos = soup.find('ul', {'class': 'unj-list-row'})
    if relacao_processos is not None:
        n_processo = relacao_processos.find_all('a', {'class':'linkProcesso'})
        classe = relacao_processos.find_all('div', {'class':'classeProcesso'})
        assunto = relacao_processos.find_all('div', {'class':'assuntoProcesso'})
        data_local= relacao_processos.find_all('div', {'class':'dataLocalDistribuicao'})

        listas = [n_processo, classe, assunto, data_local]
        texto = ''
        for i in range(len(listas[0])):
            for lista in listas:
                texto = texto + (lista[i].text.strip()) + '\n'
            texto = texto + '\n\n'    
        return texto
         
    # Encontro de um único processo
    processo_unico = soup.find('div', {'class': 'unj-entity-header__summary__barra'})
    if processo_unico is not None:
         n_processo = processo_unico.find('span', {'id':'numeroProcesso'})
         if n_processo:
             n_processo = n_processo.text.strip()
         classe = processo_unico.find('div', {'id':'classeProcesso'})
         if classe:
             classe = classe.text.strip()
         assunto = processo_unico.find('div', {'id':'assuntoProcesso'})
         if assunto:
             assunto = assunto.text.strip()
         orgao = processo_unico.find('div', {'id': 'orgaoJulgadorProcesso'})
         if orgao:
             orgao = orgao.text.strip()
            
         return(f'\n{n_processo}\n{classe}\n{assunto}\n{orgao}\n')

# Início
print('Bem vindo ao crawler do Pimentel v. 1.0')

# Verifica a existência dos arquivos "investigados.txt" e "oab.txt" na pasta "config_pesquisa".
relacao_investigados = '../config_pesquisa/investigados.txt'
relacao_oab = '../config_pesquisa/oab.txt'
condicao = os.path.exists(relacao_investigados) and os.path.exists(relacao_oab)
if(not(condicao)):
  print("Não encontrei os arquivos de configuração. Pressione Enter para sair...")
  input()
  sys.exit()

# Cria a pasta de resultados
pasta = '../_resultados'
print (f'Após a execução, procure o arquivo gerado na pasta {pasta}')

if not os.path.exists(pasta):
    os.makedirs(pasta)

# Verifica se a pasta de resultados já contém arquivos e extai o hash (SHA-1) do mais recente

# Lista de arquivos no diretório se existentes
arquivos = os.listdir(pasta)
if arquivos:
    
    # Ordena os arquivos por data de modificação
    arquivos = sorted(arquivos, key=lambda x: os.path.getmtime(os.path.join(pasta, x)))

    # Seleciona o arquivo mais recente
    arquivo_recente = os.path.join(pasta, arquivos[-1])
    
    # Calcula o hash SHA-1 do arquivo selecionado
    with open(arquivo_recente, 'rb') as arquivo:
        conteudo_do_arquivo = arquivo.read()
        sha1_arquivo_recente = hashlib.sha1(conteudo_do_arquivo).hexdigest()

# inicializa as listas vazias
investigados = []
oab = []

# Lê o arquivo de investigados e cria a lista de investigados
with open(relacao_investigados, 'r') as f:
    for investigado in f:
        investigados.append(investigado.strip())

# Lê o arquivo de OAB e cria a lista de pesquisa por OAB
with open(relacao_oab, 'r') as f:
    for registro in f:
        oab.append(registro.strip())

# Cria o arquivo txt para gravar a pesquisa
now = datetime.datetime.now()
now_formatado = now.strftime('%Y-%m-%d-%H-%M')
now_legivel = now.strftime('%d/%m/%Y - %Hh%Mmin.')
arquivo_resultado = f'{pasta}/resultado-{now_formatado}.txt'

# Abre o arquivo para gravar o resultado da consulta
with open(arquivo_resultado, 'w', encoding='utf-8') as f:
    f.write('\n\nPESQUISA POR INVESTIGADOS\n\n')

    # Percorre a lista de investigados e faz a consulta
    for investigado in investigados:
        response = consulta_por_parte(investigado)
       
        if (response.status_code == 200):
            soup = BeautifulSoup(response.content, 'html.parser')
            f.write(f'{investigado}:\n\n{faz_busca(soup)}')
            f.write('\n' + '-'* 58 + '\n')
            
        else:
            f.write(f'{investigado}:\n')
            f.write('Sem resposta do servidor. Verifique!')
            f.write('\n' + '-'* 58 + '\n')

    # Percorre a lista de advogados e faz a consulta
    f.write('\n\nPESQUISA POR OAB\n\n')
    for registro in oab:
        response = consulta_num_oab(registro)
        if (response.status_code == 200):
            soup = BeautifulSoup(response.content, 'html.parser')

            f.write(f'{registro}:\n{faz_busca(soup)}')
            f.write('\n' + '-'* 58 + '\n')
                
        else:
           f.write(f'{registro}:\n')
           f.write('Sem resposta do servidor. Verifique!')
           f.write('\n' + '-'* 58 + '\n')

# Calcula o hash SHA-1 do arquivo recém-criado
with open(arquivo_resultado, 'rb') as arquivo:
    conteudo_do_arquivo = arquivo.read()
    sha1_arquivo_resultado = hashlib.sha1(conteudo_do_arquivo).hexdigest()


# Compara o conteúdo dos arquivos recente (se existente) e resultado pelo hash
if arquivos:
    print('-'* 58)
    print("Últimos arquivos gerados | hash (sha-1)")
    print(arquivo_recente, sha1_arquivo_recente)
    print(arquivo_resultado, sha1_arquivo_resultado)
    print('-'* 58)
    if (sha1_arquivo_recente == sha1_arquivo_resultado):
        print('\nSem alteração das informações anteriores.\n')
    else:
        print('\nATENÇÃO: novas informações incluídas!\n')

print('Programa concluído!')
print("Pressione Enter para sair...")
input()