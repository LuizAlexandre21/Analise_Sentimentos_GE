from pymongo import MongoClient
import pandas as pd
from urllib.request import urlopen
from bs4 import BeautifulSoup

## Importando os links
client = MongoClient()
data= client['Jornais']
data= data['Noticias']
data = pd.DataFrame(list(data.find()))

# Extraindo textos
Titulo=[]
Subtitulo=[]
Data=[]
Texto=[]
for i in data['Url']:
    print(i)
    url=urlopen(i)
    bs = BeautifulSoup(url, 'html.parser')
    # Extraindo o titulo
    title = bs.find('div', {'class':'row content-head non-featured'})
    if title is not None:
        title = title.find('h1',{'class':'content-head__title'}).text
        #Sprint(title)
        Titulo.append(title)
        subtitle = bs.find('div',{'class':'medium-centered subtitle'}).text
        #print(subtitle)
        Subtitulo.append(subtitle)
    else:
        Titulo.append(" ")
        Subtitulo.append(" ")
    #Extraindo a data
    datas = bs.find('div',{'class':'content__signature'})
    if datas is not None:
        time=datas.find('div',{'class':'content-publication-data'}).find('p',{'class':'content-publication-data__updated'}).find('time').text
        #print(time)
        Data.append(time)
    else:
        Data.append(" ")
    #Extraindo texto
    #Primeiro Paragrafo
    article_1=bs.find('div',{'class':'mc-column content-text active-extra-styles active-capital-letter'})
    if article_1 is not None:
        text_1=article_1.find('p',{'class':'content-text__container theme-color-primary-first-letter'}).text
        #print(text_1)

    #Outros Paragrafos
    article = bs.find('div',{'class':'mc-article-body'})
    if article is not None:
        text = article.find('div',{'class':'wall protected-content'}).text
        text = text.replace("  ","")
        texto = text_1 + text
        Texto.append(texto)
    else:
        Texto.append(" ")

    # Time
data = pd.DataFrame({'Titulo':Titulo,'Subtitulo':Subtitulo,'Data':Data,'Texto':Texto,'Time':data['Clube']})

client = MongoClient()
db = client["Jornais"]
Artigo = db["Artigo"]
Artigo.insert_many(data.to_dict("records"))
