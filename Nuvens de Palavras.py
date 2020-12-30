from pymongo import MongoClient
import pandas as pd
import nltk
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import cv2
import matplotlib.colors


## WordCloud

# Importando o banco de dados
client = MongoClient()
db = client['Jornais']
data = db['Artigos_Limpos']
data = pd.DataFrame(list(data.find()))

# Times
clubes = ['athletico-pr','atletico-go','bahia','botafogo','bragantino','corinthians','flamengo','fluminense','goias','gremio','internacional','palmeiras','ceara','fortaleza','sao paulo','sport','vasco','atletico-mg']
for i in clubes:
    dados = data[data['Time']== i]

    texto = dados['Texto_limpo'].reset_index(drop=True)
    subtitulo = dados['Subtitulo_limpo'].reset_index(drop=True)
    titulo = dados['Titulo_limpo'].reset_index(drop=True)

    texto = texto[0]+texto[1]+texto[2]+texto[3]+texto[4]+texto[5]+texto[6]+texto[7]
    subtitulo = subtitulo[0]+subtitulo[1]+subtitulo[2]+subtitulo[3]+subtitulo[4]+subtitulo[5]+subtitulo[6]+subtitulo[7]
    titulo = titulo[0]+titulo[1]+titulo[2]+titulo[3]+titulo[4]+titulo[5]+titulo[6]+titulo[7]

    # Subtitulo
    plt.figure(figsize=(10,5))
    fd = nltk.FreqDist(subtitulo)
    fd.plot(30,title = "Palavras x Frequência",cumulative=False)
    # Titulo
    plt.figure(figsize=(10,5))
    fd = nltk.FreqDist(titulo)
    fd.plot(30,title = "Palavras x Frequência",cumulative=False)
    # Texto
    plt.figure(figsize=(10,5))
    fd = nltk.FreqDist(texto)
    fd.plot(30,title = "Palavras x Frequência",cumulative=False)

    text = " ".join(texto)
    title= " ".join(titulo)
    subtitle = " ".join(subtitulo)

    # Nuvem de palavras
    # Mapa Rubro - Negro
    cmap1 = matplotlib.colors.LinearSegmentedColormap.from_list("", ["red","black"])
    # Mapa gremio
    cmap2 = matplotlib.colors.LinearSegmentedColormap.from_list("",["blue","silver","black"])
    # Mapa Alvi-negro
    cmap3 = matplotlib.colors.LinearSegmentedColormap.from_list("",['black','silver'])
    # Mapa Bahia - Fortaleza
    cmap4 = matplotlib.colors.LinearSegmentedColormap.from_list("",['red','silver','blue'])
    # Mapa Bragantino
    cmap5 = matplotlib.colors.LinearSegmentedColormap.from_list("",['red','yellow','blue'])
    # Mapa - Alvi-verde
    cmap6=matplotlib.colors.LinearSegmentedColormap.from_list("",['green','silver'])
    # Mapa - São paulo
    cmap7 = matplotlib.colors.LinearSegmentedColormap.from_list("",['red','silver','black'])
    # Mapa - Fluminense
    cmap8 = matplotlib.colors.LinearSegmentedColormap.from_list("",['red','silver','green'])
    # Mapa - internacional
    cmap9 = matplotlib.colors.LinearSegmentedColormap.from_list("",['red','silver'])

    if i in ['flamengo','athletico-pr','atletico-go','sport']:
        cmap = cmap1

    elif i in ['gremio']:
        cmap = cmap2

    elif i in ['ceara','botafogo','atletico-mg','santos','vasco','corinthians']:
        cmap = cmap3

    elif i in ['bahia','fortaleza']:
        cmap = cmap4

    elif i in ['bragantino']:
        cmap = cmap5

    elif i in ['coritiba','palmeiras','goias']:
        cmap = cmap6

    elif i in ['sao paulo']:
        cmap = cmap7

    elif i in ['internacional']:
        cmap = cmap9
    else:
        cmap =cmap8

    # Importando figuras para a nuvem
    imagem = cv2.imread(i+".jpg")
    gray = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
    ret,mask = cv2.threshold(gray,250,255,cv2.THRESH_BINARY)

    # Criando a nuvem de Palavras - Titulo
    wordcloud = WordCloud(background_color="white",width=800, height=800, mask=mask, colormap=cmap, collocations = False).generate(title)
    fig = plt.figure(figsize=(20,10))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    fig.savefig(i+'_titulo', dpi=fig.dpi)
    plt.show()

    wordcloud = WordCloud(background_color="white",width=800, height=800, mask=mask, colormap=cmap, collocations = False).generate(subtitle)
    fig = plt.figure(figsize=(20,10))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    fig.savefig(i+'_subtitulo', dpi=fig.dpi)
    plt.show()

    wordcloud = WordCloud(background_color="white",width=800, height=800, mask=mask, colormap=cmap, collocations = False).generate(text)
    fig = plt.figure(figsize=(20,10))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    fig.savefig(i+'_texto', dpi=fig.dpi)
    plt.show()
