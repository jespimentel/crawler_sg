# crawler_sg
## Pesquisa processos no 2º Grau do TJSP por investigado ou advogado

### Introdução

A Promotoria de Justiça de Piracicaba monitora a entrada de processos em 2º grau relacionados a seus investigados, realizando consultas periódicas ao eSAJ, de forma automática. Para isso, criamos um web crawler (ou "robozinho") para realizar a pesquisa não autenticada ao eSAJ.

A aplicação faz buscas por nome da parte ou número de OAB e retorna informações sobre processos criminais encontrados.

A linguagem de programação escolhida foi o Python, utilizando-se as bibliotecas Requests (requisições web), BeautifulSoup (para parsear o HTML), datetime (para a manipulação de datas e horários) e os (para a manipulação de arquivos).

### Estratégias usadas no programa

O programa realiza a busca em uma URL específica e utiliza o método POST para enviar os dados necessários. Ele analisa a resposta utilizando a biblioteca BeautifulSoup e, a partir disso, retorna os resultados em um formato legível. Os arquivos de configuração armazenam as informações de investigados e números de OAB. O arquivo de resultados gravado é comparado com o atual, por meio de hash, para verificar se houve alteração nas informações anteriormente obtidas.

### Como obter o programa

O código fonte do programa está publicado no GitHub, com licença MIT (cf. em <https://github.com/jespimentel/crawler_sg>). Os iniciados em Python não terão qualquer dificuldade para clonar o programa e rodar na própria máquina. As bibliotecas necessárias estão relacionadas no arquivo "requirements.txt". Para os colegas de MP, podemos fornecer o executável, mediante solicitação (o Windows Defender pode reclamar disso...).

### Como usar o programa

Para utilizar o programa, é necessário criar dois arquivos de texto dentro da pasta "config_pesquisa": "investigados.txt" e "oab.txt". No arquivo "investigados.txt", deve-se incluir o nome das partes que se deseja buscar informações, uma em cada linha. Já no arquivo "oab.txt", deve-se incluir o número de OAB, um em cada linha. Assentos e pontos devem ser desprezados.

Após a criação dos arquivos, basta executar o programa e esperar o resultado ser gerado na pasta "_resultados".

### Limitações

Não há garantia de funcionamento, nem de resultados. Qualquer alteração no site do TJSP "quebra" a lógica do programa, que procura o resultado contido em tags específicas da página html de resultados. 

### Conclusões 

O programa é uma ferramenta útil para a coleta automatizada das informações sobre processos judiciais, limitada a consulta ao 2º Grau do Tribunal de Justiça do Estado de São Paulo, através do portal eSAJ e para um usuário não autenticado.

---
Para saber mais sobre a construção de crawlers com Python, Requests e BeautifulSoup, consulte: https://www.digitalocean.com/community/tutorials/como-fazer-scraping-em-paginas-web-com-beautiful-soup-and-python-3-pt. Acesso em: 21 abr. 2023.
