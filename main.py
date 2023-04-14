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

# Verifica a existência dos arquivos "investigados.txt" e "oab.txt".
# Caso não existam, sai do programa
import os.path
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

print(investigados)
print(oab)

# Cria o arquivo txt para gravar a pesquisa (com a data/hora)
now = datetime.datetime.now()
now_formatado = now.strftime('%Y-%m-%d-%H-%m')
now_legivel = now.strftime('%d/%m/%Y - %Hh%mmin')
arquivo_resultado = 'resultado-' + now_formatado +'.txt'
with open(arquivo_resultado, 'w') as f:
    f.write(f'RESULTADO DA VARREDURA REALIZADA EM {now_legivel}')
    f.write('\n' + '-'* 58 + '\n\n')

# Percorre a lista de investigados e faz a consulta por partes
for investigado in investigados:
    response = consulta_por_parte(investigado)
    if (response.status_code == 200):
        soup = BeautifulSoup(response.content, 'html.parser')
        if (soup.find('div', {'id':'spwTabelaMensagem'})):
            print('Encontrei uma mensagem')
        else:
            if (soup.find('div', {'id': 'listagemDeProcessos'})):
                print('Encontrei a listagem de processos')

        
    else:
        with open(arquivo_resultado, 'a') as f:
            f.write(f'{investigado}: ')
            f.write('sem resposta do servidor. Verifique!')
            f.write('\n' + '-'* 58 + '\n')





# Verifica o "response" e grava o alerta em arquivo texto para != 200

# Cria o objeto BeautifulSoup a partir do conteúdo HTML da resposta
# soup = BeautifulSoup(response.content, 'html.parser')



# Grava o resultado da pesquisa (Não foram encontrados..., Muitos processos..., Único processo, Relação de processos)
# Percorre a lista de OAB e faz a consulta por advogado
# Testa o "response" e grava o alerta em arquivo texto para != 200
# Grava o resultado da pesquisa (verificar opções / testar tb com nomes)
# Transformar em executável para a distribuição (não usar a opção de arquivo único)

""" 

with open('resultado.txt', 'w') as arquivo:
    for linha in linhas:
        conteudo = search_parte(linha)
        print(linha, file=arquivo)
        # Alerta: não foram encontrados processos ou foram encontrados muitos processos
        try:
            listagem_de_processos = conteudo.find('div', {'id':'spwTabelaMensagem'})
            print(listagem_de_processos.get_text().strip(), file=arquivo)
        except:
            # Encontro de um único processo (o eSAJ já abre na página correspondente)
            try:
                listagem_de_processos = conteudo.find('div', {'class':'unj-entity-header__summary__barra'}) 
                print(listagem_de_processos.get_text().strip(), file=arquivo)
            except:
                try:
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
                except:
                        print(f'Verifique manualmente o nome informado\n', file=arquivo)
        print('*'*30, file=arquivo)

print('Programa concluído!') """