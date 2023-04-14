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
    mensagem = soup.find('div', {'id': 'spwTabelaMensagem'})
    if mensagem is not None:
        texto = mensagem.find('td', {'id':'mensagemRetorno'})
        texto = texto.find('li').get_text()
        return texto
    
    relacao_processos = soup.find('div', {'id': 'listagemDeProcessos'})
    if relacao_processos is not None:
        return('Encontrei uma lista de processos')
         
    processo_unico = soup.find('div', {'class': 'container'})
    if processo_unico is not None:
         return('Encontrei uma lista de processos')


# Verifica a existência dos arquivos "investigados.txt" e "oab.txt".
# Caso não existam, sai do programa
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

# Cria o arquivo txt para gravar a pesquisa (com a data/hora)
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
            f.write(f'{investigado}:\n{faz_busca(soup)}')
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

# Tarefas
# Readme
# Transformar em executável para a distribuição (não usar a opção de arquivo único)

""" 
# Encontro de vários processos na primeira página
listagem_de_processos = conteudo.find('div', {'id': 'listagemDeProcessos'})

# Encontra todas as tags filhas da tag `listagem_de_processos`
n_processo = listagem_de_processos.find('a', {'class':'linkProcesso'})
classe = listagem_de_processos.find('div', {'class':'classeProcesso'})
assunto = listagem_de_processos.find('div', {'class':'assuntoProcesso'})
data_local= listagem_de_processos.find('div', {'class':'dataLocalDistribuicao'})

print(n_processo.get_text().strip(), file=arquivo)
print(classe.get_text().strip(), file=arquivo)
print(assunto.get_text().strip(), file=arquivo)
print(data_local.get_text().strip(), file=arquivo)
            
"""