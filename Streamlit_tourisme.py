import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(layout="wide")

title1, title2 = st.columns([0.7, 0.3])

with title1 :
  st.title('Projet Tourisme : Recherche de lieux touristiques variés')
with title2 :
  "Julie" 
  st.image('image_lille.jpg')

#####


st.title('Choix de la région')

st.write("Il nous a été demandé premièrement de nettoyer et analyser une base de données contenant les caractérisqtiques de nombreux films, et d'en extraire une selection à proposer à un cinéma Français en perte de vitesse.")

#Chargement du DataFrame étudié :
df = pd.read_csv('ech.csv')

col1_df, col2_df = st.columns([0.7, 0.3])

with col1_df :
  f"Voici un échantillon aléatoire de 20 lieux, qui contient {df.shape[0]} lignes :"
  df_sample = df[['Nom_du_POI', 'Categories_de_POI','Description', 'Ville','nom_departement', 'nom_region']].set_axis(['Nom', 'Catégories', 'Description', 'Ville', 'Département', 'Région'], axis = 1).sample(20)
  df_sample

with col2_df :
  "Types de lieux disponibles :"
  df_sample['Categories_de_POI'].value_counts()
  df_sample['Categories_de_POI'].uniques()

st.title('Ajustement de la selection')

"Nous vous proposons d'effectuer une sélection selon les critères de votre choix :"

types_lieux = []

for index, row in df_sample.iterrows():
  for i in row["Categories_de_POI"] :
    if i not in types_lieux :
      types_lieux.append(i)

types_lieux.sort()

col_types, col_region, col_dep = st.columns(3)

with col_types :  
  types_lieux = ['(tous)'] + types_lieux
  type_lieux = st.selectbox("Type de lieu :", types_lieux)

with col_region : 
  regs = ['(tous)'] + [i for i in df_sample["nom_region"]]
  reg = st.selectbox("Région :", regs)

with col_dep :
  deps = ['(tous)'] + [i for i in df_sample["nom_departement"]]
  dep = st.selectbox("Département :", deps)


  
if type_lieux != "(tous)" :
  select = df_sample[(df_sample['Categories_de_POI'].str.contains(type_lieux))]
if type_lieux == "(tous)" :
  select = df_sample

if reg != "(tous)" :
  select = select[select['nom_region'] == reg]

if dep != "(tous)" :
  select = select[select['nom_departement'] == dep]



st.title('votre sélection :')

f"Les critères sélectionnés réduisent votre sélection à {select.shape[0]} lieux :"


select
