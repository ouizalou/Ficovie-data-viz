
# =====================================================================================
# 📊 SCRIPT : Analyse des données FICOVIE - Contrats d'assurance vie
# 🗂️ Chargement des données depuis Excel et nettoyage des doublons/incohérences
# 📈 Visualisations multiples avec Seaborn, Matplotlib et Plotly (2D, 3D, interactives)
# 🧠 Analyse des montants versés, durées, compagnies, statuts et souscripteurs
# 🗃️ Génération automatique d’un rapport PDF professionnel avec FPDF
# 💡 Objectif : offrir une vue claire, synthétique et visuelle des contrats FICOVIE
# 💾 Sauvegarde des graphiques en PNG/HTML et export des données en Excel
# =====================================================================================


import pandas as pd

import datetime as DT

# 🗂️ random un module permet de générer des nombres et des choix aléatoires
import random as rd

# 🗂️ matplotlib bibliotheque de visualisation de données pour creer des graphique et pyplot fournit une interface de haut niveau
import matplotlib.pyplot as plt

# 🗂️ seaborn bibliothéque permet de visualiser des données basé sur matplotlib , et rendre les graphiques plus simple
import seaborn as sbn

# 🗂️ permet de personaliser les valeurs affichées sur les axes d'un graphique
import matplotlib.ticker as ticker

# 🗂️ bbq qui perment de créer des graphiques intéractifs et élegants
import plotly.express as px

# 🗂️  qui perment de créer des graphiques 3D
import plotly.graph_objects as go

# 🗂️ reportlab est bbq qui permet de generer des fichiers PDF / pagesizes --> format de la page (A4) ET letter --> la taille de la page(8,5X11 pouces)
from reportlab.lib.pagesizes import letter

# 🗂️ colors --> permet de fournir un ensemble de couleurs prédéfinies pour créer un PDF
from reportlab.lib import colors

# 🗂️ canvas --> permet de créer et dessiner directement sur un fichier PDF 
from reportlab.pdfgen import canvas

# 🗂️ inch facilite la gestion des marges et distances 
from reportlab.lib.units import inch

# io permet de travailler avec des flux(memoire , fichier) dans le cas reportlab -->> pour generer un PDF en memoire au lieux de l'enregistrer en disque
import io

# fpdf permet de generer des documents PDF de maniere simple
from fpdf import FPDF

# 🗂️ permet d'interagir avec le système d'exploitation pour manipuler des fichiers des repertoires et obtenir des infos sur système
import os

# créer une variable pour le fichier excel
assurance_excel="FICOVIE.xlsx"
# lecture de fichier excel
print("\n 🧾 chargement des données de fichier excel ficovie : \n")

try:
    DF=pd.read_excel(assurance_excel)
    print(DF.head())
except FileNotFoundError:
    print(f" \n ❌ erreur le fichier : {assurance_excel} est introvable ")
    exit()

id_con=input("\n 📝 veuillez saisir le numéro de contrat de souscripteur rechercher : ")
if not id_con:
    print("\n ❌  erreur, veuillez saisir à nouveau un numéro valide: \n ")
    exit()
print(DF[DF["Numéro de contrat"]==id_con])

# filtrer les lignes les contrat > 100 000£ ou ceux de la banque AXA
print("\n 🔍 les lignes les contrat > 100 000£ ou ceux de la banque AXA: ")
contrat=DF[(DF["Montant versé"]>100000 ) | (DF["Banque / Compagnie"]== "AXA")]
print(contrat)

# filtrer les souscripteur dont le contrat est assurance de vie
print("\n 🔍 les souscripeteur dont le contrat est assurance de vie sont : \n")
sousc=DF[DF["Type de contrat"]=="Assurance Vie"]
print(sousc[["Numéro de contrat","Nom du souscripteur","Montant versé","Type de contrat","Banque / Compagnie"]])

# filtrer les souscripteur dont le contrat est assurance de vie
print("\n 🔍 les souscripeteur dont le contrat est Contrat de Capitalisation de vie sont : \n")
sousc=DF[DF["Type de contrat"]=="Contrat de Capitalisation"]
print(sousc[["Numéro de contrat","Nom du souscripteur","Montant versé","Type de contrat","Banque / Compagnie"]])

# trier les donnees de fichier ficovie par montant versé
print("\n 📌 le trie des souscripteur par le montant versé : \n")
DF=DF.sort_values(by="Montant versé")
print(DF[["Numéro de contrat","Nom du souscripteur","Montant versé","Type de contrat"]])

# trier les donnees de fichier ficovie par montant versé, date souscription,nom de souscripteur
print("\n 📌 le trie des souscripteur par leur nom, montant versé, date de souscription : \n")
DF=DF.sort_values(by=["Montant versé","Nom du souscripteur","Type de contrat","Date de souscription"])
print(DF[["Numéro de contrat","Nom du souscripteur","Montant versé","Type de contrat","Date de souscription"]])

# ajouter une colonne statut de contrat << Si la date de souscription est plus de 10 ans "clôturé" sinon "actif"
today=DT.datetime.today()
DF["Statut du contrat"]=(today-DF["Date de souscription"]).dt.days // 365
DF["Statut du contrat"]=DF["Statut du contrat"].apply(lambda x:"clôturé" if x>= 10 else "actif")

# ajouter une colonne mode de versement avec choix aléatoire
# liste de mode de virsement 
modes_de_versement = ["Unique", "Mensuel", "Trimestriel", "Annuel", "Périodique"]
# la methode rd.choice retourne une valeur au hasard parmi une liste
DF["Mode de versement"]=[rd.choice(modes_de_versement) for _ in range(len(DF))] 

# explorer le fichier
try:
    DF.to_excel("ficovies.xlsx",index=False)
    print("\n ✅ Les données ont été sauvegardées dans 'ficovies.xlsx'.")
except Exception as e:
    print(f"\n ❌ Erreur lors de l'enregistrement du fichier : {e}")
    exit()


# regrouper les données par compagnie , par type de contrat et calculer des totaux.

print("\n 📋 regroupement par companie et de type de contrat en calculant les moyennes : \n")
moyenne_montant=DF.groupby(["Banque / Compagnie","Type de contrat"])["Montant versé"].mean()
print(moyenne_montant)

# regrouper les données par compagnie , par type de contrat et calculer des totaux.

print("\n 📋 regroupement par companie et de type de contrat en calculant les totaux : \n")
DF["totaux_montant"]=DF.groupby(["Banque / Compagnie","Type de contrat"])["Montant versé"].transform("sum")
print(DF)

# Moyenne des montants, plus gros contrat, nombre de contrats par compagnie

print("\n 📈 moyennes des montants par compagnie : \n")
moyenne_par_compagnie=DF.groupby(["Banque / Compagnie"])["Montant versé"].mean()
print(moyenne_par_compagnie)

print("\n 💎 l'index du plus gros contrat global :\n")
plus_gros_contrat=DF.loc[DF["Montant versé"].idxmax()]
print(plus_gros_contrat)

print("\n 🏆 le plus gros contrat par compagnie :\n")
plus_gros_contrat=DF.groupby(["Banque / Compagnie"])["Montant versé"].max()
print(plus_gros_contrat)

# filtrer les contrat appartenant a plusieurs compagnies
print("\n 🔎 les contrats de compagnie maif, macif,allianz, et AXA :\n ")

# isin() une methode de pandas verifie si les element de la liste sont present  dans la colonne banque/compagnie
compagnie_cibles=["Maif","Macif","Allianz","AXA"]
contrat_filtre=DF[DF["Banque / Compagnie"].isin(compagnie_cibles)] 
print(contrat_filtre)

# filtrer les contrats dont le type de contrat contient le mot "vie"
print("\n 🔎 les contrats dont le type de contrat contient le mot vie : ")

# str.contains() utilisé sur les colonne dont le type est chaine de caractere permet de verifier si une chaine contient un mot ou une expression
# case= pour respecter la casse(majuscule /minuscule) ,na= si la case contient des valeurs manquante (Nan), regex= expression reguliere
type_contrat_filtre=DF[DF["Type de contrat"].str.contains("vie",case=False,na=False,regex=True)]
print(type_contrat_filtre)

# filtrer les contrat dont le montant versé >100 000£ chez AXA ou BNP
print("\n 🔍 le montant versé >100 000£ chez AXA ou BNP :")
# query() permet de filtrer des lignes en ecrivant des conditions
resultats_contrat = DF.query("`Montant versé` > 100000 and `Banque / Compagnie` in ['AXA', 'BNP']")
print(resultats_contrat)

#  La méthode merge() en Pandas te permet de combiner deux DataFrames comme en SQL (JOIN)
print("\n 🔗 Fusion des infos DF assurnce et compagnie_DF :\n")

# creer un datafarme df2
compagnie_DF=pd.DataFrame({"Banque / Compagnie": ["AXA", "Macif", "Maif"],
                           "Téléphone": ["01 23 45 67 89", "01 98 76 54 32", "01 11 22 33 44"]})

#  faire la jointure avec la DF assurance /how --> type de jointure (inner, left, right), on--> la colonne commune utilisé pour la jointure
DF_avec_infos=pd.merge(DF,compagnie_DF,how="left",on="Banque / Compagnie")
print(DF_avec_infos)

# lecture de fichier banque_compagnie DF2
print("\n 🧾 chargement des données de fichier excel banque_compagnie : \n")
banque_comp="banque_compagnie.xlsx"
try:
    DF2=pd.read_excel(banque_comp)
    print(DF2)
except FileNotFoundError:
    print(f" \n ❌ erreur le fichier : {banque_comp} est introvable ")
    exit()

print("\n 🔗 Fusion des infos des deux DataFarme assurance DF et banque_compagnie DF2 :\n")
# jointure sur la colonne banque/ compagnie
DF["Banque / Compagnie"] = DF["Banque / Compagnie"].str.strip()
DF2["Banque / Compagnie"] = DF2["Banque / Compagnie"].str.strip()

DF_fusion_excel=pd.merge(DF,DF2,how="left",on="Banque / Compagnie")
print(DF_fusion_excel.head())

# sauvegarder le resultat dans un fichier excel
try:
    DF_fusion_excel.to_excel("ficovie_merge_banque.xlsx",index=False)
    print("\n ✅ Les données ont été sauvegardées dans 'ficovie__merge_banque.xlsx'.")
except Exception as e:
    print(f"\n ❌ Erreur lors de l'enregistrement du fichier : {e}")
    exit()

# faire une jointure entre DF et DF2
# set_index() permet de definir la colonne comme index de DataFarme 
DF2.set_index("Banque / Compagnie", inplace=True) # inplace permet de modifier directement l'index de DataFarme

DF_joint_DF2=DF.join(DF2, how="left", on="Banque / Compagnie")

# sauvegarder le resultat avec join() dans un fichier excel
try:
    DF_joint_DF2.to_excel("ficovie_join_banque.xlsx",index=False)
    print("\n ✅ Les données ont été sauvegardées dans 'ficovie_join_banque.xlsx'.")
except Exception as e:
    print(f"\n ❌ Erreur lors de l'enregistrement du fichier : {e}")
    exit()

print("\n 📊 Nombre de contrats par compagnie : \n")
nombre_de_contrat=DF["Banque / Compagnie"].value_counts()
print(nombre_de_contrat)


print("\n 📊 création des graphique avec les bibliothéques matplotlib, seaborn, plotly \n")

# ====================================== 📊 visualisation des données ==================================

GRAPH_DIR='graphs'      # dossier contenant les images .png nommées par numéro de contrat
os.makedirs(GRAPH_DIR,exist_ok=True)

somme_par_compagnie=DF.groupby(["Banque / Compagnie"])["Montant versé"].sum()
# definir la taille de la figure(largeur,hauteur)
plt.figure(figsize=(8 , 6))

# tracer un graphe a barres horizontales et coleur blue
somme_par_compagnie.plot(kind="bar",color="green")
plt.title("  Somme des montants versés par compagnie ")
plt.ylabel(" Montant total (£) ")
plt.xlabel(" Banque / Compagnie ")

# ajuster automatiquement les elements du graphique
plt.tight_layout()
# affiche le graphique
print("\n 📊 affichage du graphique : \n")
#plt.show()
plt.savefig(os.path.join(GRAPH_DIR, "Somme_des_montants_par_compagnie.png"))  # changer le nom pour chaque graphique
plt.close()


print("\n 📊 visualisation de la répartition des types de contrat : \n")
def repartition_par_contrat(DF):
    try:
        repartition_type=DF["Type de contrat"].value_counts()
        print(repartition_type)
        plt.figure(figsize=(6,6))
        # autopct --> permet de spécifier le format d'affichage des porcentage ET %1.1f%% --->affiche le resultat en decimal 
        # startangle ---> fait en sorte que la première part du camembert commence en haut a 90 
        # la plt.cm.Pastel1 ---> est une palette de couleurs pastel douce de Matplotlib
        repartition_type.plot(kind="pie", autopct="%1.1f%%", startangle=90, colors=plt.cm.Pastel1.colors )
        plt.title(" Répartition des types de contrat ")
        plt.ylabel("")
        plt.tight_layout()
        #plt.show()
        if not os.path.exists(GRAPH_DIR):
            os.makedirs(GRAPH_DIR)

        graph_path=os.path.join(GRAPH_DIR, "Répartition_des_types_de_contrat.png") # changer le nom pour chaque graphique
        plt.savefig(graph_path)
        plt.close()
        return graph_path
    except Exception as e:
        print(f"Erreur dans creer_graphique_contrats_par_annee: {e}")
        return None
# appel de la fonction
repartition_par_contrat(DF)
print("\n 📈 l'analyse de l'evolution des montants versés par mois ")

## transformer la colonne en dateet errors='coerce' signifie que si une valeur ne peut pas être convertie en une date valide,
#  cette valeur sera remplacée par NaT (Not a Time), qui est l'équivalent de NaN pour les dates dans Pandas.
DF["Date de souscription"]=pd.to_datetime(DF["Date de souscription"], errors="coerce")

# vérifier si des dates invalides ou manquantes existent dans la colonne "Date de souscription" 

if DF["Date de souscription"].isnull().any():
    print("\n ❗❗ Attention : certaines dates sont invalides. ")
    exit()

# grouper l'evolution par mois et sommer les montants versé
evolution=DF.groupby(DF["Date de souscription"].dt.to_period("M"))["Montant versé"].sum()
print(evolution)
plt.figure(figsize=(6,6))
# marker="o" ajouter des cercles commme marquers sur chaque point de la courbe , teal est la couleur blue vert
evolution.plot(marker="o", color="teal") 
plt.title(" Evolution des montants versés par mois ")
plt.xlabel(" Mois ")
plt.ylabel(" Montant total ")
plt.tight_layout()
#plt.show()
plt.savefig(os.path.join(GRAPH_DIR, "Evolution_des_montants_versés_par_mois.png"))  # changer le nom pour chaque graphique
plt.close()

 
# création d'une carte thermique qui peremet de visualiser la correlation (relation) entre plusieurs variable numerique
# dans un tableau en utilisant une échelle de couleurs
plt.figure(figsize=(8,6))
# heatmap() est une methode de seaborn qui permet d'afficher une carte thérmique a partir d'une matrice de données
# annot= permet d'activer l'affichage des nombres dans chaque cellule
sbn.heatmap(DF.corr(numeric_only=True), annot=True,cmap="coolwarm")     # cmap= palatte des couleurs
plt.title(" \n corrélation entre les variables numériques")
# 1 corrélation parfaite positive / -1 corrélation parfaite negative / 0 pas de corrélation 
#plt.show()
plt.savefig(os.path.join(GRAPH_DIR, "corrélation_entre_les_variables_numériques.png"))  # changer le nom pour chaque graphique
plt.close()


#calculer la corrélation 
print(" \n 📈 matrice de corrélation: /n")
matrice_corr=DF[["Montant versé","totaux_montant"]].corr()
print(matrice_corr)

plt.figure(figsize=(8,6))
sbn.heatmap(matrice_corr, annot=True,cmap="viridis", linewidths=0.5, fmt=".2f") # linewidths :ligne blanche entre les cases
plt.title(" corrélation entre le montant versé et les montaux totaux ")
#plt.show()
plt.savefig(os.path.join(GRAPH_DIR, "corrélation_entre_le_montant_versé_et_les_montaux_totaux.png"))  # changer le nom pour chaque graphique
plt.close()


# =========================visualisation d'un histogramme avec histplot de seaborn==================================

plt.figure(figsize=(8,6))
# bins nombre de barres  / kde= estimation de distribution 
sbn.histplot(DF["Montant versé"],bins=30, kde=True, color="skyblue")
plt.title(" Distribution des montants versés ")
plt.xlabel(" Montant versé (£)")
plt.ylabel("Nombre de contrats")

# cibler les axes pour personnaliser l'affichage avec £
axes=plt.gca()
# xaxis.set_major_locator  permet de definir l'emplacement des ticks sur l'axe x (tous les 50000)
axes.xaxis.set_major_locator(ticker.MultipleLocator(50000))
# la methode .xaxis.set_major_formatter permet de configurer les proprietés des axes dans une figure 
# format des ticks avec "k" (milliers)
axes.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{int(x/1000)}K£"))
#axes.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{int(x):,} £"))

plt.tight_layout()
#plt.show()
plt.savefig(os.path.join(GRAPH_DIR, "Distribution_des_montants_versés.png"))  # changer le nom pour chaque graphique
plt.close()

# boxplot
plt.figure(figsize=(6,4))
sbn.boxplot(y=DF["Montant versé"],data=DF, palette="viridis",notch=True)
plt.xticks(rotation=45)
plt.title(" Boxplot de montant versé ")
plt.ylabel(" montant versé")
plt.tight_layout()
#plt.show()
plt.savefig(os.path.join(GRAPH_DIR, "Boxplot_de_montant_versé.png"))  # changer le nom pour chaque graphique
plt.close()

plt.figure(figsize=(10,8))
sbn.boxplot(data=DF,x="Banque / Compagnie",y="Montant versé",palette="magma")
# graphique de point permet de visualiser la distribution des données stripplot
sbn.stripplot(x="Banque / Compagnie",y="Montant versé",data=DF,color="red",size=5,jitter=True)
plt.xticks(rotation=45)
plt.title(" Le montant versé par compagnie")
plt.tight_layout()
#plt.show()
plt.savefig(os.path.join(GRAPH_DIR, "Le_montant_versé_par_compagnie.png"))  # changer le nom pour chaque graphique
plt.close()


plt.figure(figsize=(10,8))
sbn.boxplot(data=DF,x="Type de contrat",y="Montant versé",hue="Mode de versement",palette="Pastel2",showfliers=False)
sbn.stripplot(data=DF,x="Type de contrat",y="Montant versé",hue="Mode de versement",dodge=True,color="black",size=5,jitter=True,alpha=0.5)
plt.title(" Le montant versé par contrat et mode de versement ")
plt.xticks(rotation=45)
# bbox_to_anchor=(1.05,1) ---> la position de la legende sur le graphique ET loc='upper left' --> ajuster le point d'accroche sur la  legende
plt.legend(title=" Le montant versé par contrat et mode de versement ",bbox_to_anchor=(1.05,1),loc='upper left')
plt.tight_layout()
#plt.show()
plt.savefig(os.path.join(GRAPH_DIR, "Le_montant_versé_par_contrat_et_mode_de_versement.png"))  # changer le nom pour chaque graphique
plt.close()


plt.figure(figsize=(10,8))
sbn.violinplot(data=DF,x="Type de contrat",y="Montant versé",hue="Statut du contrat",palette="Pastel2",split=True,inner="quartile")
plt.title(" Le montant versé par contrat et Statut du contrat (violinplot) ")
plt.xticks(rotation=45)
# bbox_to_anchor=(1.05,1) ---> la position de la legende sur le graphique ET loc='upper left' --> ajuster le point d'accroche sur la  legende
plt.legend(title=" Le montant versé par contrat et Statut du contrat ",bbox_to_anchor=(1.05,1),loc='upper left')
plt.tight_layout()
#plt.show()
plt.savefig(os.path.join(GRAPH_DIR, "Le_montant_versé_par_contrat_et_Statut_du_contrat.png"))  # changer le nom pour chaque graphique
plt.close()

print("\n 📈 les statistique de montant versé :\n")
describe_stat=DF.groupby("Banque / Compagnie")["Montant versé"].describe()
print(describe_stat)
describe_stat.to_excel("statistique_montant_par_compagnie.xlsx")


# pairplot permet de visualiser toutes les relations entre plusieurs variables numériques sous forme de nuages de points + histogrammes
colonne_numeriques=DF[["Montant versé","totaux_montant"]]
g=sbn.pairplot(colonne_numeriques)
g.fig.set_size_inches(11,8)
g.fig.suptitle("pairplot des montant versé", y=0.99,fontsize=14)
g.fig.tight_layout()
#plt.show()
plt.savefig(os.path.join(GRAPH_DIR, "pairplot_des_montants_versé.png"))  # changer le nom pour chaque graphique
plt.close()

sbn.pairplot(DF, vars=["Montant versé", "totaux_montant"], hue="Banque / Compagnie")
plt.suptitle("pairplot des montant versé par compagnie", y=0.99)
#plt.show()
plt.savefig(os.path.join(GRAPH_DIR, "pairplot_des_montants_versé_par_compagnie.png"))  # changer le nom pour chaque graphique
plt.close()


# visualisation interactive des données avec plotly
fig=px.box(
    DF,
    x="Banque / Compagnie",
    y="Montant versé",
    color="Mode de versement",
    title=" Le montant versé par compagnie",
    points="all", #
    notched=True)
# la methode update_layout permet de personnaliser le graphique
# xaxis_tickangle permet de pivoter les etiquettes de l'axe x
fig.update_layout( xaxis_tickangle=-45)

fig.show()
fig.write_html("plot_interactif_montant_par_compagnie.html")
print("✅ Fichier HTML interactif sauvegardé.")
somme_par_compagnie=DF.groupby(["Banque / Compagnie"])["Montant versé"].sum().reset_index()     # reset.index() --> reinitialiser l'index

fig2=px.bar(
    somme_par_compagnie,
    x="Banque / Compagnie",
    y="Montant versé",
    color="Banque / Compagnie",
    title=" Somme des montants versés par compagnie")
fig2.update_layout(xaxis_tickangle=-45)
fig2.write_html("plot_interactif_montant_par_compagnie2.html")
print("✅ Fichier HTML interactif sauvegardé.")
fig2.show()

DF["Date de souscription"]=pd.to_datetime(DF["Date de souscription"],errors="coerce")
DF["Annee"]=DF["Date de souscription"].dt.year
DF["Duree du contrat"]=(DT.datetime.today()-DF["Date de souscription"]).dt.days/365
DF["Duree du contrat"]=DF["Duree du contrat"].round(1)
fig=go.Figure(data=[go.Scatter3d(
    x=DF["Montant versé"],
    y=DF["Annee"],
    z=DF["Duree du contrat"],
    mode='lines+markers',
    marker=dict(size=5,color=DF["Montant versé"],colorscale='viridis',opacity=0.8),
    text=DF["Banque / Compagnie"])])
fig.update_layout(xaxis_tickangle=-45,title=" Graphique 3D des contrats d'assurance",
                  scene=dict(xaxis_title="Montant versé",yaxis_title="Annnée de souscription",zaxis_title="Durée du contrat"))
fig.show()
fig.write_html("plot_interactif_montant_et_duree_de_contrat_par_compagnie.html")
print("✅ Fichier HTML interactif sauvegardé.")
DF.to_excel("Ficovies_annnee.xlsx",index=False)

print("\n Répartition par contrat \n ")

def repartition_par_compagnie(DF):
    try:
        repartition_montants = DF.groupby("Banque / Compagnie")["Montant versé"].sum()
        print(repartition_montants)

        plt.figure(figsize=(8,6))
        repartition_montants.plot(kind="bar", color=plt.cm.Pastel1.colors)
        plt.title("Répartition des montants par compagnie")
        plt.ylabel("Montant total versé (€)")
        plt.xlabel("Banque / Compagnie")
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()

        if not os.path.exists(GRAPH_DIR):
            os.makedirs(GRAPH_DIR)

        graph_path = os.path.join(GRAPH_DIR, "Répartition des montants par compagnie.png")
        plt.savefig(graph_path)
        plt.close()
        return graph_path

    except Exception as e:
        print(f"Erreur dans repartition_par_contrat: {e}")
        return None
repartition_par_compagnie(DF)


def creer_graphique_contrats_par_annee(df):
    try:
        contrats_par_annee = df["Annee"].value_counts().sort_index()
        plt.figure(figsize=(10, 6))
        contrats_par_annee.plot(kind='bar', color='skyblue')
        plt.title('Nombre de contrats par année')
        plt.xlabel('Année')
        plt.ylabel('Nombre de contrats')
        plt.tight_layout()

        # Créer le dossier s'il n'existe pas
        if not os.path.exists(GRAPH_DIR):
            os.makedirs(GRAPH_DIR)

        # Sauvegarde du graphique
        graph_path = os.path.join(GRAPH_DIR, "graph_contrats_par_annee.png")
        plt.savefig(graph_path)
        plt.close()
        return graph_path
    except Exception as e:
        print(f"Erreur dans creer_graphique_contrats_par_annee: {e}")
        return None

# appel de la fonction
creer_graphique_contrats_par_annee(DF)

fig = px.scatter_3d(
    DF,
    x="Montant versé",
    y="Annee",
    z="Duree du contrat",
    color="Montant versé",
    animation_frame="Annee",  # Animation par année
    hover_name="Banque / Compagnie",
    color_continuous_scale="viridis",
    size_max=10,
    opacity=0.7,
)
fig.update_layout(title="Évolution des contrats d'assurance dans le temps")
fig.show()
fig.write_html("plot_interactif_Évolution_des_contrats_d'assurance_dans_le_temps.html")
print("✅ Fichier HTML interactif sauvegardé.")

fig = px.scatter_3d(
    DF,
    x="Montant versé",
    y="Annee",
    z="Duree du contrat",
    color="Banque / Compagnie",  # Chaque banque a sa couleur
    hover_name="Nom du souscripteur", # afficher nom de souscripteur
    symbol="Type de contrat"
)
fig.update_layout(title="Contrats d’assurance par banque/compagnie")
fig.show()
fig.write_html("contrats_d'assurance_par_banque_compagnie.html")
print("✅ Fichier HTML interactif sauvegardé.")

# nettoyage des donnees 
def nettoyer_donnees(DF) :
    DF=DF.copy()
    DF.columns=DF.columns.str.strip()
    DF.drop_duplicates(subset="Numéro de contrat",inplace=True)
    DF.dropna(subset=["Numéro de contrat","Nom du souscripteur"],inplace=True)
    return DF
# appel de la fonction nettoyer_donnees
nettoyer_donnees(DF)


 # ====================================================== PDF Rapport ===============================================================

# === CONFIGURATION ===
EXCEL_FILE="ficovie_merge_banque.xlsx"

OUTPUT_DIR='rapports_pdf'


# Créer le dossier de sortie s’il n’existe pas
os.makedirs(OUTPUT_DIR,exist_ok=True)
os.makedirs(GRAPH_DIR,exist_ok=True)
# === LECTURE DU FICHIER EXCEL ===
DF = pd.read_excel(EXCEL_FILE)


# Chargement de votre DataFrame (exemple avec un fichier Excel)
assurances_excel = "ficovies.xlsx"
DF1 = pd.read_excel(assurances_excel)

# Définition des chemins pour les graphiques et la sortie
GRAPH_DIR = "graphs"
OUTPUT_DIR = "path_to_output"
# Ajout des polices Roboto
if not os.path.exists(GRAPH_DIR):
    os.makedirs(GRAPH_DIR)
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

print("\n 📄 genération d'un rapport pdf << analyse-ficovies>> automatique \n")
def generer_pdf(DF1) :
    class PDFReport(FPDF):
    # fonction pour créer l'entête de pdf
        def header(self):
            self.set_font("Roboto", "B", 12)
            self.cell(0, 10, "Rapport d'Analyse - FICOVIE", border=False, ln=True, align="C")
            self.ln(10)
    # fonction pour créer pied de page de pdf
        def footer(self):
            self.set_y(-15)
            self.set_font("Roboto", "I", 8)
            self.cell(0, 10, f'Page {self.page_no()}', align='C')
    # fonction pour créer le titre de chapitre
        def chapter_title(self, title):
            self.set_font("Roboto", "B", 12)
            self.set_text_color(0, 0, 128)
            self.cell(0, 10, title, ln=True)
            self.ln(4)
    # fonction pour créer le contenu de chapitre
        def chapter_body(self, text):
            self.set_font("Roboto", "", 11)
            self.set_text_color(0, 0, 0)
            self.multi_cell(0, 10, text)
            self.ln()
    # fonction pour inserer des images 
        def insert_image(self, image_path, width=180):
            if os.path.exists(image_path):
                self.image(image_path, w=width)
                self.ln(10)
    # fonction pour créer la table des matiere de pdf
        def table_of_contents(self):
            self.chapter_title("Table des matières")
            self.chapter_body(""" 
            1. Synthèse des contrats
            2. Top 5 des montants versés
            3. Graphiques
            """)

    # Création du PDF
    pdf = PDFReport()
    # Ajout des polices Roboto
    pdf.add_font('Roboto', '', 'fonts/Roboto-Regular.ttf', uni=True)  # Regular
    pdf.add_font('Roboto', 'B', 'fonts/Roboto-Bold.ttf', uni=True)  # Bold
    pdf.add_font('Roboto', 'I', 'fonts/Roboto-Italic.ttf', uni=True)  # Italic
    pdf.add_page()

    # Utilisation de la police Roboto
    pdf.set_font('Roboto', '', 12)

    # Titre et date
    pdf.set_font("Roboto", "B", 16)
    pdf.cell(0, 10, "Rapport d'Analyse de Données - FICOVIE", ln=True, align="C")
    pdf.set_font("Roboto", "", 12)
    pdf.cell(0, 10, f"Date : {DT.datetime.now().strftime('%d/%m/%Y')}", ln=True, align="C")
    pdf.ln(20)

    # Table des matières
    pdf.table_of_contents()

    # Synthèse
    pdf.chapter_title("1. Synthèse des contrats")
    pdf.chapter_body(f"""
    Nombre total de contrats : {len(DF1)}
    Nombre de contrats actifs : {DF1[DF1["Statut du contrat"] == "actif"].shape[0]}
    Nombre de contrats clôturés : {DF1[DF1["Statut du contrat"] == "clôturé"].shape[0]}
    """)

    # Top 5 montants
    top5 = DF1.groupby("Nom du souscripteur")["Montant versé"].sum().nlargest(5)
    pdf.chapter_title("2. Top 5 des montants versés")
    for i, (nom, montant) in enumerate(top5.items(), 1):
        pdf.chapter_body(f"{i}. {nom} - {montant:.2f} €")

    # ajouter des Graphiques au PDF
    pdf.chapter_title("3. Graphiques")
    pdf.insert_image(os.path.join(GRAPH_DIR, "graph_contrats_par_annee.png"))
    pdf.insert_image(os.path.join(GRAPH_DIR, "Répartition_des_types_de_contrat.png"))
    pdf.insert_image(os.path.join(GRAPH_DIR,"Distribution_des_montants_versés.png"))
    pdf.insert_image(os.path.join(GRAPH_DIR,"Le_montant_versé_par_contrat_et_mode_de_versement.png"))
    pdf.insert_image(os.path.join(GRAPH_DIR,"Evolution_des_montants_versés_par_mois.png"))
    pdf.insert_image(os.path.join(GRAPH_DIR,"pairplot_des_montants_versé_par_compagnie.png"))

    # Ajouter une Conclusion
    pdf.chapter_title("4. Conclusion")
    pdf.chapter_body("Ceci est la conclusion du rapport. Les informations et les graphiques ont été générés à partir des données fournies.")

    # Sauvegarde
    pdf_path = os.path.join(OUTPUT_DIR, "rapport_ficovie.pdf")
    pdf.output(pdf_path)

    print(f"PDF généré : {pdf_path}")
    return pdf_path
# appel de la fonction generer un rapport pdf
generer_pdf(DF1)

"""
        # filtre selection multiple des compagnie
        compagnies = DF["Banque / Compagnie"].unique()
        compagnie_selectionnee=st.multiselect("🏦 Sélectionnez une ou plusieurs compagnies d'assurance pour filtrer :"
                                              ,options=compagnies,default=compagnies)
        if compagnie_selectionnee:
            #isin() pour filtrer les lignes du DataFrame où la colonne "Banque / Compagnie" contient l'une des compagnies sélectionnées dans la liste compagnie_selectionnee.
            donnees_filtrees=DF[DF["Banque / Compagnie"].isin(compagnie_selectionnee)]
            # ', '.join(compagnie_selectionnee) pour afficher un message contenant les noms des compagnies sélectionnées.
            st.subheader(f"📋 Contrats pour les compagnies sélectionnées : {', '.join(compagnie_selectionnee)}")
            st.dataframe(donnees_filtrees[["Numéro de contrat", "Nom du souscripteur", "Type de contrat", "Montant versé"]])
        else:
            st.info("📝 Aucune compagnie sélectionnée, toutes les données sont affichées.")"""
