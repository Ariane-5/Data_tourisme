import streamlit as st
import pandas as pd
import numpy as np

import folium
from branca.element import Figure

#from streamlit_folium import st_folium

st.set_page_config(layout="wide")

title1, title2 = st.columns([0.7, 0.3])

with title1 :
  st.title('Tourisme (en cours de développement)')
  st.write("Base de données présentant des lieux touristiques variés. En cours de développement... (c'est pas pour demain, cependant... ^^)")
  st.write("Source des données : https://www.data.gouv.fr/datasets/datatourisme-la-base-nationale-des-donnees-publiques-dinformation-touristique-en-open-data. Je n'invente rien et je ne suis pas non plus opératrice de saisie 🤡)")
  
  st.write("Mise à jour du 11/02/2025 : Ajout d'un bouton pour valider la sélection des critères avant le chargement de la suite, afin d'optimiser ou ne pas dégrader les performances. Chargement des données actualisées à ce jour, pour la région Hauts-de-France (la finalité étant de proposer la France métropolitaine entière, si cela n'est pas trop lourd...)")
  st.write("Mise à jour du 15/02/2025 : Quelques modifications de l'apparence. Ajout des données Ile-de-France. Taille max de fichier : 25MB... A voir plus tard pour l'ajout des autres régions.")

with title2 :
  st.image('image_lille.jpg')
  st.write('Julie')

#####


st.title('Aperçu aléatoire')

#Chargement du DataFrame étudié :
df = pd.read_csv('ech.csv',
    dtype={
        "nom_region": "category",
        "nom_departement": "category"}
    )

df.drop_duplicates(inplace=True)

# Remettre la colonne des POI et clean2 au format liste :
import ast
df['Categories_de_POI'] = df['Categories_de_POI'].apply(ast.literal_eval)
#df['clean2'] = df['clean2'].apply(ast.literal_eval)

# Remettre les colonnes des départements et CP au format texte :
#df['DEP'] = df['DEP'].astype('str')
df['CP'] = df['CP'].astype('str')

#col1_df, col2_df = st.columns([0.7, 0.3])

ech = df[df["Description"].notna()].sample(3)

#with col1_df :
f"3 lieux au hasard, sur les {df.shape[0]} présents :"


cols = st.columns(3)

for col, (_, row) in zip(cols, ech.iterrows()):

    with col:
        st.markdown(
            f"""
            <div style="
                border:1px solid #ddd;
                padding:12px;
                border-radius:10px;
                background-color:#fafafa;
                color:#222;
            ">
                <h4 style="margin-bottom:6px;">{row['nom_region']} - {row['nom_departement']}</h4>
                <p><b>{row['Nom_du_POI']}</b></p>
                <p style="font-size:0.9em;">{row['Description']}</p>
                <p style="font-size:0.8em; color:#555;">
                    {row['Contacts_du_POI']}
                </p>
                <p style="font-size:0.8em; color:#555;">
                    {row['Adresse_postale']} - {row['CP']} - {row['Ville']}
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )



#with col2_df :
  #"Types de lieux disponibles :"
  
types_lieux = []

for index, row in df.iterrows():
  for i in row["Categories_de_POI"] :
    if i not in types_lieux :
      types_lieux.append(i)

types_lieux.sort()

st.title('Critères de selection')

with st.form("filtres"):

  col_types, col_region, col_dep, col_ville = st.columns(4)

  with col_types :  
    types_lieux = types_lieux
    type_lieu = st.multiselect("Type de lieu :", types_lieux)

  with col_region : 
    regs = [i for i in df["nom_region"]]
    regs = set(regs)
    regs = sorted(regs)
    reg = st.multiselect("Région :", regs)

  with col_dep :
    deps = [i for i in df["nom_departement"]]
    deps = set(deps)
    deps = sorted(deps)
    dep = st.multiselect("Département :", deps)

  with col_ville :
    villes = [i for i in df["Ville"]]
    villes = set(villes)
    villes = sorted(villes)
    ville = st.multiselect("Ville :", villes)

  submit = st.form_submit_button("🔍 Appliquer les filtres")
  
select = df.copy()

if submit:

  if type_lieu:
      select = select[select["Categories_de_POI"].apply(lambda x: any(t in x for t in type_lieu))]

  if reg:
      select = select[select["nom_region"].isin(reg)]

  if dep:
      select = select[select["nom_departement"].isin(dep)]

  if ville:
        select = select[select["Ville"].isin(ville)]

  st.write(f"Lignes correspondantes : {select.shape[0]}")

  if len(select) > 200 : 
      st.write('Ça fait beaucoup là... Tu testes mes limites ? Tout repose sur ta connexion...')


  st.title('Résultats')

  # ************ Ajout 28/11/2025 ************

  # ************ CARTE ************

  if len(select) > 0 :
    
    f"Les critères sélectionnés réduisent votre sélection à {select.shape[0]} lieu(x) :"

    st.dataframe(select[['Nom_du_POI', 'Categories_de_POI','Description', 'Ville','nom_departement', 'nom_region']].set_axis(['Nom', 'Catégories', 'Description', 'Ville', 'Département', 'Région'], axis = 1))

    fig = Figure(width=1200, height=700)

    #Utiliser la moyenne des latitudes et longitudes pour centrer la carte :

    lat_moy = select['Latitude'].mean()
    lon_moy = select['Longitude'].mean()

    map = folium.Map(location = [lat_moy, lon_moy], zoom_start=10, control_scale=True)

    for index, location_info in select.iterrows():
        try :
          etiquette = '\n'.join([location_info['Nom_du_POI'], location_info['Contacts_du_POI']])
          folium.Marker([location_info["Latitude"], location_info["Longitude"]], popup=etiquette).add_to(map)
        except :
          continue

    fig.add_child(map)
    
    #st_folium(map)
    
    st.components.v1.html(folium.Figure().add_child(map).render(), height=500)

  else :
    print('\n --- Pas de résultat :( ---')

  # ************ WORDCLOUD ************

