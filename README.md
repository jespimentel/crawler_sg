# crawler_sg
## Pesquisa processos no 2º Grau do TJSP por investigado ou advogado



### Introdução

A Promotoria monitora a entrada de processos em 2º grau relacionados a seus investigados, realizando consultas periódicas ao eSAJ manualmente. Para automatizar essa tarefa, criamos o presente web crawler para a pesquisa não autenticada ao 2º Grau do Tribunal de Justiça do Estado de São Paulo. 

A aplicação faz buscas por nome da parte ou número de OAB e retorna informações sobre processos criminais encontrados. 

A linguagem de programação escolhida foi o Python, utilizando-se as bibliotecas Requests (requisições web), BeautifulSoup (para parsear o HTML), datetime (para a manipulação de datas e horários) e os (para a manipulação de arquivos).

### Estratégias usadas no programa

O programa realiza a busca em uma URL específica e utiliza o método POST para enviar os dados necessários. Ele analisa a resposta utilizando a biblioteca BeautifulSoup e, a partir disso, retorna os resultados em um formato legível. O programa também utiliza arquivos de configuração para armazenar as informações de investigados e números de OAB, além de criar uma pasta para armazenar os resultados.

### Como usar o programa
Para utilizar o programa, é necessário criar dois arquivos de texto dentro da pasta "config_pesquisa": "investigados.txt" e "oab.txt". No arquivo "investigados.txt", deve-se incluir o nome das partes que se deseja buscar informações, uma em cada linha. Já no arquivo "oab.txt", deve-se incluir o número de OAB, um em cada linha. Assentos e pontos devem ser desprezados.

Após a criação dos arquivos, basta executar o programa e esperar o resultado ser gerado na pasta "_resultados".

### Conclusões
O programa é uma ferramenta útil para a coleta automatizada das informações sobre processos judiciais, limitada a consulta ao 2º Grau do Tribunal de Justiça do Estado de São Paulo, através do portal eSAJ e para um usuário não autenticado. 

---
Para saber mais: <https://www.digitalocean.com/community/tutorials/como-fazer-scraping-em-paginas-web-com-beautiful-soup-and-python-3-pt>. Acesso em: 15 abr. 2023.
