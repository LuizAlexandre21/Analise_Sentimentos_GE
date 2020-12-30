import pandas as pd
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
from pymongo import MongoClient


client = MongoClient()
data = client['Jornais']
data = data['Artigo']
data = pd.DataFrame(list(data.find()))

texto = data['Texto'].reset_index(drop=True)
titulo = data['Titulo'].reset_index(drop=True)
subtitulo = data['Subtitulo'].reset_index(drop=True)

sentimento_text = []
p_pos_text = []
p_neg_text = []
for i in texto:
    blob = TextBlob(i, analyzer=NaiveBayesAnalyzer())
    sentimento_text.append(blob.sentiment[0])
    p_pos_text.append(blob.sentiment[1])
    p_neg_text.append(blob.sentiment[2])
    print("tops")

sentimento_titulo = []
p_pos_titulo = []
p_neg_titulo = []
for i in titulo:
    blob = TextBlob(i, analyzer=NaiveBayesAnalyzer())
    sentimento_titulo.append(blob.sentiment[0])
    p_pos_titulo.append(blob.sentiment[1])
    p_neg_titulo.append(blob.sentiment[2])
    print("tops")

sentimento_subtitulo = []
p_pos_subtitulo = []
p_neg_subtitulo = []
for i in subtitulo:
    blob = TextBlob(i, analyzer=NaiveBayesAnalyzer())
    sentimento_subtitulo.append(blob.sentiment[0])
    p_pos_subtitulo.append(blob.sentiment[1])
    p_neg_subtitulo.append(blob.sentiment[2])
    print("tops")


data['Sentimento_text']= sentimento_text
data['p_pos_text'] = p_pos_text
data['p_neg_text']= p_neg_text
data['Sentimento_titulo']= sentimento_titulo
data['p_pos_titulo'] = p_pos_titulo
data['p_neg_titulo']= p_neg_titulo
data['sentimento_subtitulo']= sentimento_subtitulo
data['p_pos_subtitulo'] = p_pos_subtitulo
data['p_neg_subtitulo']= p_neg_subtitulo


client = MongoClient()
db = client["Jornais"]
Sentimento = db["Sentimento"]
Sentimento.insert_many(data.to_dict("records"))
