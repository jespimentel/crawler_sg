import sys
import os.path
import datetime
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
# Verifica a existência dos arquivos "investigados.txt" e "oab.txt" na pasta "config_pesquisa".
condicao = os.path.exists('config_pesquisa/investigados.txt') and os.path.exists('config_pesquisa/oab.txt')
if(not(condicao)):
  sys.exit()

# inicializa as listas vazias
investigados = []
oab = []

# Lê o arquivo de investigados e cria a lista de investigados
with open('config_pesquisa/investigados.txt', 'r') as f:
    for investigado in f:
        investigados.append(investigado.strip())

# Lê o arquivo de OAB e cria a lista de pesquisa por OAB
with open('config_pesquisa/oab.txt', 'r') as f:
    for registro in f:
        oab.append(registro.strip())

# Cria o arquivo txt para gravar a pesquisa
now = datetime.datetime.now()
now_formatado = now.strftime('%Y-%m-%d-%H-%M')
now_legivel = now.strftime('%d/%m/%Y - %Hh%Mmin.')
arquivo_resultado = f'resultado-{now_formatado}.txt'

# Abre o arquivo para gravar o resultado da consulta
with open(arquivo_resultado, 'w', encoding='utf-8') as f:
    f.write(f'RESULTADO DA VARREDURA REALIZADA EM {now_legivel}\n')
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

print('Programa concluído!')