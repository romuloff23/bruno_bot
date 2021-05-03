#Autor Rômulo Farias
import time
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import csv
import re
from selenium.common.exceptions import WebDriverException
from datetime import date
import os.path
#configurações padrão
data_atual = date.today()
option = Options()
option.headless = True
driver = webdriver.Firefox()

#dicionario de URL e Estado
URLs = {
    "Total":"https://www.catho.com.br/vagas/?pais_id=31&q=programador",
    "SP":"https://www.catho.com.br/vagas/programador/sp/?q=Programador&estado_id%5B0%5D=25",
    "RJ":"https://www.catho.com.br/vagas/programador/rj/?q=Programador&estado_id%5B0%5D=19",
    "MG":"https://www.catho.com.br/vagas/programador/mg/?q=Programador&estado_id%5B0%5D=13",
    "RS":"https://www.catho.com.br/vagas/programador/rs/?q=Programador&estado_id%5B0%5D=21",
    "PR":"https://www.catho.com.br/vagas/programador/pr/?q=Programador&estado_id%5B0%5D=16",
    "SC":"https://www.catho.com.br/vagas/programador/sc/?q=Programador&estado_id%5B0%5D=24",
    "MT":"https://www.catho.com.br/vagas/programador/mt/?q=Programador&estado_id%5B0%5D=11",
    "MS":"https://www.catho.com.br/vagas/programador/ms/?q=Programador&estado_id%5B0%5D=12",
    "GO":"https://www.catho.com.br/vagas/programador/go/?q=Programador&estado_id%5B0%5D=9",
    "DF":"https://www.catho.com.br/vagas/programador/df/?q=Programador&estado_id%5B0%5D=7",
    "AM":"https://www.catho.com.br/vagas/programador/am/?q=Programador&estado_id%5B0%5D=4",
    "PA":"https://www.catho.com.br/vagas/programador/pa/?q=Programador&estado_id%5B0%5D=14",
    "AC":"https://www.catho.com.br/vagas/programador/ac/?q=Programador&estado_id%5B0%5D=1",
    "RO":"https://www.catho.com.br/vagas/programador/ro/?q=Programador&estado_id%5B0%5D=22",
    "RR":"https://www.catho.com.br/vagas/programador/rr/?q=Programador&estado_id%5B0%5D=23",
    "AP":"https://www.catho.com.br/vagas/programador/ap/?q=Programador&estado_id%5B0%5D=3",
    "TO":"https://www.catho.com.br/vagas/programador/to/?q=Programador&estado_id%5B0%5D=27",
    "BA":"https://www.catho.com.br/vagas/programador/ba/?q=Programador&estado_id%5B0%5D=5",
    "CE":"https://www.catho.com.br/vagas/programador/ce/?q=Programador&estado_id%5B0%5D=6",
    "PE":"https://www.catho.com.br/vagas/programador/pe/?q=Programador&estado_id%5B0%5D=17",
    "MA":"https://www.catho.com.br/vagas/programador/ma/?q=Programador&estado_id%5B0%5D=10",
    "AL":"https://www.catho.com.br/vagas/programador/al/?q=Programador&estado_id%5B0%5D=2",
    "RN":"https://www.catho.com.br/vagas/programador/rn/?q=Programador&estado_id%5B0%5D=20",
    "PI":"https://www.catho.com.br/vagas/programador/pi/?q=Programador&estado_id%5B0%5D=18",
    "PB":"https://www.catho.com.br/vagas/programador/pb/?q=Programador&estado_id%5B0%5D=15",
    "SE":"https://www.catho.com.br/vagas/programador/se/?q=Programador&estado_id%5B0%5D=26"
}
#dicionario que recebe  valores
Valores = {
    "Total" : "",
    "SP": "",
    "RJ":"",
    "MG":"",
    "RS":"",
    "PR":"",
    "SC":"",
    "MT":"",
    "MS":"",
    "GO":"",
    "DF":"",
    "AM":"",
    "PA":"",
    "AC":"",
    "RO":"",
    "RR":"",
    "AP":"",
    "TO":"",
    "BA":"",
    "CE":"",
    "PE":"",
    "MA":"",
    "AL":"",
    "RN":"",
    "PI":"",
    "PB":"",
    "SE":""
}

#dicionari de regiões
sudeste = {
    'sudeste':0,
    'SP':0,
    'RJ':0,
    'MG':0
}

sul = {
    'sul':0,
    'RS':0,
    'PR':0,
    'SC':0
}

centroOeste = {
    'centroOeste':0,
    'MT':0,
    'MS':0,
    'GO':0,
    'DF':0
}

norte = {
    'norte':0,
    'AM':0,
    'PA':0,
    'AC':0,
    'RO':0,
    'RR':0,
    'AP':0,
    'TO':0
}
nordeste = {
    'nordeste':0,
    'BA':0,
    'CE':0,
    'PE':0,
    'MA':0,
    'AL':0,
    'RN':0,
    'PI':0,
    'PB':0,
    'SE':0
}
#faz busca

def execultarBuscar(url):
    print(url)
    driver.get(url)
    time.sleep(5)
    try:
        element = driver.find_element_by_id('jobTitle')
        html_content = element.get_attribute('outerHTML')
        pretratada = html_content.replace("h1","")
        dado = re.sub('[^0-9]', '', str(pretratada))
        return dado
    except WebDriverException as erro: 
        return 0
#varre
def varrerURL():
    for url in URLs:
        Valores[url]= execultarBuscar(URLs[url])


#calculo porcentual por região 
def separacaoDeRegiao(nome,regiao):
    #carregar dados do Valores para sua região especifica.
    for key in regiao:
        if(key in Valores):
            regiao[key] = int(Valores[key])
    #somatoria da regiao.
    for key in regiao:
        regiao[nome] += int(regiao[key])
    return regiao


#Salvado em arquivo CSV
def salvar():
    header = {
        "data":data_atual,
        "Brasil":Valores['Total']
    }
    joi = {**header,**sul, **sudeste, **centroOeste, **norte, **nordeste}
    if(os.path.exists('dados.csv')):
        print("Adicionando dados")
        with open ('dados.csv','a',newline='') as file:
            writer = csv.writer(file,delimiter=',')  
            writer.writerow(joi.values())
    else:
        print("Criando arquivo")
        with open ('dados.csv','w',newline='') as file:
            writer = csv.writer(file,delimiter=',')  
            writer.writerow(joi.keys())
            writer.writerow(joi.values())
#chamando a fução para coleta dos dadados
varrerURL()
driver.quit()
#repassando os dados para cada região com sua %
sul = separacaoDeRegiao("sul",sul)
sudeste = separacaoDeRegiao("sudeste",sudeste)
centroOeste = separacaoDeRegiao("centroOeste",centroOeste)
norte = separacaoDeRegiao("norte",norte)
nordeste = separacaoDeRegiao("nordeste",nordeste)
#salvando os dados em arquivo 
salvar()


print("===================================================================")
print("Execução encerrada, todos os dados foram salvos em um arquivo csv ")
print("===================================================================")
