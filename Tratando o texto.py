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
#stopwords = [de,a,o,que,e,do,da,em,um,para,é,com,não,uma,os,no,se,na,por,mais,as,dos,como,mas,foi,ao,ele,das,tem,à,seu,sua,ou,ser,quando,muito,há,nos,já,está,eu,também,só,pelo,pela,até,isso,ela,entre,era,depois,sem,mesmo,aos,ter.seus,quem,nas,me,esse,eles,estão,você,tinha,foram,essa,num,nem,suas,meu,às,minha,têm,numa,pelos,elas,havia,seja,qual,será,nós,tenho,lhe,deles,essas,esses,pelas,este,fosse,dele,tu,te,vocês,vos,lhes,meus,minhas,teu,tua,teus,tuas,nosso,nossa,nossos,nossas,dela,delas,esta,estes,estas,aquele,aquela,aqueles,aquelas,isto,aquilo,estou,está,estamos,estão,estive,esteve,estivemos,estiveram,estava,estávamos,estavam,estivera,estivéramos,esteja,estejamos,estejam,estivesse,estivéssemos,estivessem,estiver,estivermos,estiverem,hei.há,havemos,hão,houve,houvemos,houveram,houvera,houvéramos,haja,hajamos,hajam,houvesse,houvéssemos,houvessem,houver,houvermos,houverem,houverei,houverá,houveremos,houverão,houveria,houveríamos,houveriam,sou,somos,são,era,éramos,eram,fui,foi,fomos,foram,fora,fôramos,seja,sejamos,sejam,fosse,fôssemos,fossem,for,formos,forem,serei,será,seremos,serão,seria,seríamos,seriam,tenho,tem,temos,tém,tinha,tínhamos,tinham,tive,teve,tivemos,tiveram,tivera,tivéramos,tenha,tenhamos,tenham,tivesse,tivéssemos,tivessem,tiver,tivermos,tiverem,terei,terá,teremos,terão,teria,teríamos,teriam]


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
