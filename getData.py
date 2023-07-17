import requests
from bs4 import BeautifulSoup

def getResults():
    #variables
    tableResult = {
        'PTM':[],
        'PT':[],
        'PTV':[],
        'PTN':[],
        'FED':[],
        'COR':[]
    }

    dateResult = ''

    #Obtendo a table do website
    table = getTable()

    #Encontrando o cabeçalho separadamente
    caption = table.find('caption')

    dateResult = caption.text

    #Encontrando o cabeçalho separadamente
    tHead = table.find('thead')

    #Separando as colunas com os nomes dos sorteios
    tableHeadCollumns = tHead.find_all('th') # Colunas de 0 a 5

    #Separando o corpo da tabela
    tbody = table.find('tbody') #Linhas de 0 a 6 e colunas de 0 a 5

    #Separando as linhas do corpo da tabela
    tRows = tbody.find_all('tr')

    #variavel para acompanhar o for de preenchimento do objeto com os resultados
    index = 0

    #For para percorrer os itens separados da tabela e preencher o objeto resultado
    
    for value in tableHeadCollumns:
        if value.text != "": #Ignorar a primeira coluna com a indicação de qual prêmio que é
            tableResult[f'{value.text}'].append(tRows[0].find_all('td')[index].text)
            tableResult[f'{value.text}'].append(tRows[1].find_all('td')[index].text)
            tableResult[f'{value.text}'].append(tRows[2].find_all('td')[index].text)
            tableResult[f'{value.text}'].append(tRows[3].find_all('td')[index].text)
            tableResult[f'{value.text}'].append(tRows[4].find_all('td')[index].text)
            tableResult[f'{value.text}'].append(tRows[5].find_all('td')[index].text)
            tableResult[f'{value.text}'].append(tRows[6].find_all('td')[index].text)
        index+=1

    returnObjectResult = {
        'tableResult':tableResult,
        'dateResult' : dateResult
    }
    return returnObjectResult

def getTable():
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5.1 Safari/605.1.15'}
    
    #Request para o site
    response = requests.get('https://www.ojogodobicho.com/deu_no_poste.html', headers=headers)

    #Primeiro parse do site completo
    site = BeautifulSoup(response.text, "html.parser")

    #Separando a Tabela de resultados completamente
    table = site.find('table', attrs={'class':'twelve'})

    return table