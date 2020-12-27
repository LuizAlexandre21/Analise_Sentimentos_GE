from pymongo import MongoClient
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import pandas as pd
import re
import nltk

# Funções

def lower(lista):
    low=[]
    for i in lista:
        low.append(i.lower())
    return low


# Importando o Banco de dados

client = MongoClient()
data = client['Jornais']
data = data['Artigo']
data = pd.DataFrame(list(data.find()))

# Limpando os Textos
# Removendo linhas repetidas
data=data.drop_duplicates(subset=['Texto'])

# Tokenização do texto e stopwords
Texto =[]
Titulo=[]
Subtitulo=[]

for i in data.columns:
    if i == '_id':
        continue
    elif i == 'Data':
        continue
    elif i =='Texto':
        for k in data['Texto']:
            Texto.append(word_tokenize(k))

    elif i =='Titulo':
        for k in data['Titulo']:
            Titulo.append(word_tokenize(k))

    elif i =='Subtitulo':
        for k in data['Subtitulo']:
            Subtitulo.append(word_tokenize(k))



# Trocando a Caixa
Texto_lw = []
Titulo_lw = []
Subtitulo_lw = []

for i in Texto:
    Texto_lw.append(lower(i))

for i in Titulo:
    Titulo_lw.append(lower(i))

for i in Subtitulo:
    Subtitulo_lw.append(lower(i))

# Removendo as stopwords
stopwords = nltk.corpus.stopwords

Texto_cl=[]
Titulo_cl=[]
Subtitulo_cl=[]

for j in Texto_lw:
    if j is not stopwords.words('portuguese'):
        Texto_cl.append(j)

for j in Titulo_lw:
    if j is not stopwords.words('portuguese'):
        Titulo_cl.append(j)

for j in Subtitulo_lw:
    if j is not stopwords.words('portuguese'):
        Subtitulo_cl.append(j)



#Criando um banco novo
data['Texto_limpo'] = Texto_cl
data['Titulo_limpo'] = Titulo_cl
data['Subtitulo_limpo'] = Subtitulo_cl

client = MongoClient()
db = client["Jornais"]
artigos = db["Artigos_Limpos"]
artigos.insert_many(data.to_dict("records"))
