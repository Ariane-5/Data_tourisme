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

st.write("Je vous propose de trouver des lieux touristiques selon les critères de votre choix, notamment le type de lieu, la région et le département (recherche par mots-clé à venir).")

st.title('Aperçu')

#Chargement du DataFrame étudié :
df = pd.read_csv('ech.csv')

# Remettre la colonne des POI et clean2 au format liste :
import ast
df['Categories_de_POI'] = df['Categories_de_POI'].apply(ast.literal_eval)
df['clean2'] = df['clean2'].apply(ast.literal_eval)

# Remettre les colonnes des départements et CP au format texte :
df['DEP'] = df['DEP'].astype('str')
df['CP'] = df['CP'].astype('str')

df.head(5)

col1_df, col2_df = st.columns([0.7, 0.3])

with col1_df :
  f"Voici un échantillon aléatoire de 20 lieux, qui contient {df.shape[0]} lignes :"
  df_sample = df[['Nom_du_POI', 'Categories_de_POI','Description', 'Ville','nom_departement', 'nom_region']].set_axis(['Nom', 'Catégories', 'Description', 'Ville', 'Département', 'Région'], axis = 1).sample(20)
  df_sample

with col2_df :
  "Types de lieux disponibles :"
  
  types_lieux = []

  for index, row in df.iterrows():
    for i in row["Categories_de_POI"] :
      if i not in types_lieux :
        types_lieux.append(i)

  types_lieux.sort()

  types_lieux

st.title('Critères deselection')

"Nous vous proposons d'effectuer une sélection selon les critères de votre choix :"


col_types, col_region, col_dep = st.columns(3)

with col_types :  
  types_lieux = ['(tous)'] + types_lieux
  type_lieux = st.selectbox("Type de lieu :", types_lieux)

with col_region : 
  regs = ['(tous)'] + [i for i in df["nom_region"]]
  regs = set(regs)
  regs = sorted(regs)
  reg = st.selectbox("Région :", regs)

with col_dep :
  deps = ['(tous)'] + [i for i in df["nom_departement"]]
  deps = set(deps)
  deps = sorted(deps)
  dep = st.selectbox("Département :", deps)


  
if type_lieux != "(tous)" :
  select = df[(df['Categories_de_POI'].str.contains(type_lieux, case=False, na=False))]
if type_lieux == "(tous)" :
  select = df

if reg != "(tous)" :
  select = select[select['nom_region'] == reg]

if dep != "(tous)" :
  select = select[select['nom_departement'] == dep]



st.title('votre sélection :')

f"Les critères sélectionnés réduisent votre sélection à {select.shape[0]} lieux :"

select
