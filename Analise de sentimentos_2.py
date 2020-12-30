from pymongo import MongoClient
import matplotlib.pyplot as plt
import matplotlib.colors
import pandas as pd
import numpy as np


## Analise de Sentimentos

# Importando os sentimentos
client = MongoClient()
db = client['Jornais']
sent=db['Sentimento']
sent = pd.DataFrame(list(sent.find()))


# Titulo

# Descobrindo o Sentimentos predominantes
sent['p_sent_titulo'] = sent['p_pos_titulo']-sent['p_neg_titulo']

sentimento_tit=[]
# Salvando o sentimento
for i in sent['p_sent_titulo']:
    if i>0.1:
        sentimento_tit.append('Pos')
    elif i< -0.1:
        sentimento_tit.append('Neg')
    else:
        sentimento_tit.append('Neutro')

sent['Novo_sentimento_titulo']=sentimento_tit


# Subtitulo

sent['p_sent_subtitulo'] = sent['p_pos_subtitulo']-sent['p_neg_subtitulo']

sentimento_subtit=[]
# Salvando o sentimento
for i in sent['p_sent_subtitulo']:
    if i>0.1:
        sentimento_subtit.append('Pos')
    elif i< -0.1:
        sentimento_subtit.append('Neg')
    else:
        sentimento_subtit.append('Neutro')

sent['Novo_sentimento_subtitulo']=sentimento_subtit


# Texto
sent['p_sent_text'] = sent['p_pos_text']-sent['p_neg_text']

sentimento_text=[]
# Salvando o sentimento
for i in sent['p_sent_text']:
    if i>0.1:
        sentimento_text.append('Pos')
    elif i< -0.1:
        sentimento_text.append('Neg')
    else:
        sentimento_text.append('Neutro')

sent['Novo_sentimento_texto']=sentimento_text


# Contabilizando os sentimentos por time

positivos_tit=[]
negativos_tit=[]
neutros_tit=[]
positivos_subtit=[]
negativos_subtit=[]
neutros_subtit=[]
positivos_tex=[]
negativos_tex=[]
neutros_tex=[]

clube = ['athletico-pr','atletico-go','bahia','botafogo','bragantino','corinthians','flamengo','fluminense','goias','gremio','internacional','palmeiras','ceara','fortaleza','sao-paulo','sport','vasco','atletico-mg']

for i in clube:

    data_tit=sent[sent['Time']==i]['Novo_sentimento_titulo'].to_list()
    data_subtit=sent[sent['Time']==i]['Novo_sentimento_subtitulo'].to_list()
    data_tex=sent[sent['Time']==i]['Novo_sentimento_texto'].to_list()
    positivos_tit.append(data_tit.count('Pos'))
    positivos_subtit.append(data_subtit.count('Pos'))
    positivos_tex.append(data_tex.count('Pos'))
    negativos_tit.append(data_tit.count('Neg'))
    negativos_subtit.append(data_subtit.count('Neg'))
    negativos_tex.append(data_tex.count('Neg'))
    neutros_tit.append(data_tit.count('Neutro'))
    neutros_subtit.append(data_subtit.count('Neutro'))
    neutros_tex.append(data_tex.count('Neutro'))


fig, ax = plt.subplots()

ax.bar(clube,positivos_tit,0.5,label='Positivos',color='springgreen')
ax.bar(clube,negativos_tit,0.5,bottom=positivos_tit,label='Negativos',color='maroon')
ax.bar(clube, neutros_tit, 0.5, bottom=np.array(negativos_tit)+np.array(positivos_tit),color='cornflowerblue')
plt.xticks(rotation=45, ha='right')
plt.ylim(0,15)
plt.legend(['Positivo','Negativos','Neutros'])
plt.ylabel("Numero de Noticias")
plt.title("Sentimentos dos Titulos das Noticias ")
plt.show()

fig, ax = plt.subplots()

ax.bar(clube,positivos_subtit,0.5,label='Positivos',color='springgreen')
ax.bar(clube,negativos_subtit,0.5,bottom=positivos_subtit,label='Negativos',color='maroon')
ax.bar(clube, neutros_subtit, 0.5, bottom=np.array(negativos_subtit)+np.array(positivos_subtit),color='cornflowerblue')
plt.xticks(rotation=45, ha='right')
plt.ylim(0,15)
plt.legend(['Positivo','Negativos','Neutros'])
plt.ylabel("Numero de Noticias")
plt.title("Sentimentos dos Subtitulos das Noticias ")
plt.show()

fig, ax = plt.subplots()

ax.bar(clube,positivos_tex,0.5,label='Positivos',color='springgreen')
ax.bar(clube,negativos_tex,0.5,bottom=positivos_tex,label='Negativos',color='maroon')
ax.bar(clube, neutros_tex, 0.5, bottom=np.array(negativos_tex)+np.array(positivos_tex),color='cornflowerblue')
plt.xticks(rotation=45, ha='right')
plt.ylim(0,15)
plt.legend(['Positivo','Negativos','Neutros'])
plt.ylabel("Numero de Noticias")
plt.title("Sentimentos dos Textos das Noticias ")
plt.show()


clube = ['athletico-pr','atletico-go','bahia','botafogo','bragantino','corinthians','flamengo','fluminense','goias','gremio','internacional','palmeiras','ceara','fortaleza','sao-paulo','sport','vasco','atletico-mg']

# Desempenho nas ultimas rodadas x sentimentos
vitorias=[2,2,0,1,1,4,4,1,2,3,3,3,3,0,4,1,1,3]
derrotas=[3,2,5,4,2,0,0,2,2,3,3,3,3,0,1,3,3,3]

np.corrcoef(vitorias,positivos_tex)
plt.scatter(vitorias,positivos_tex)
plt.show()
np.corrcoef(derrotas,negativos_tex)
plt.scatter(derrotas,negativos_tex)
plt.show()
