# =====================================================================================
# 🌐 SCRIPT : Application Web d'Analyse des Contrats FICOVIE avec Streamlit
# 🛡️ OBJECTIF :
#     - Analyser les contrats d'assurance (FICOVIE) à partir d'un fichier Excel
#     - Nettoyer et filtrer les données par type de contrat, compagnie, montant, date
#     - Visualiser les tendances et répartitions avec des graphiques générés automatiquement
#     - Générer un rapport PDF personnalisé téléchargeable
#
# 🧰 TECHNOLOGIES :
#     - Streamlit : Interface web interactive
#     - Pandas : Manipulation de données
#     - Matplotlib / Seaborn : Visualisation
#     - FPDF : Génération de rapport PDF
#     - Tkinter (dans module externe) : Interaction utilisateur (si applicable)
#
# 📁 FONCTIONNALITÉS :
#     - Téléversement de fichiers Excel
#     - Aperçu et nettoyage automatique des données
#     - Filtres dynamiques (par contrat, montant, compagnie, année, date, souscripteur)
#     - Graphiques interactifs (types de contrats, montants par compagnie, évolution annuelle)
#     - Génération et téléchargement d’un rapport PDF

# =====================================================================================




# 🗂️ permet de creer des application web interactives 
import streamlit as st
import datetime as DT
import pandas as pd
from ficovie_analyse import nettoyer_donnees, creer_graphique_contrats_par_annee, generer_pdf,repartition_par_contrat,repartition_par_compagnie
import os

#configurer l'aparence et les paramètres de la page web
st.set_page_config(page_title="Analyse FICOVIE",layout="wide")
st.title(" 📊🧐 Analyse des contrats FICOVIE  ")

# ajouter un champ de téléversement pour upload le fichier excel
uploaded_file=st.file_uploader("📂 Importer un fichier Excel",type=["xlsx"])

if uploaded_file:
    try:
        DF=pd.read_excel(uploaded_file)
        DF=nettoyer_donnees(DF)
        # Message de succès lorsque les données sont chargées et nettoyées
        st.success(" 🧹✅ Données chargées et nettoyées !")
        # Affichage d'un aperçu des premières lignes du DataFrame
        st.subheader("🧑‍💻 Aperçu des données")
        st.dataframe(DF.head())
        # Option pour filtrer les contrats "Assurance Vie"
        if st.sidebar.checkbox("🛡️  Afficher uniquement les souscripteurs avec un contrat 'Assurance Vie'",key="assurance_vie_checkbox"):
            sousc=DF[DF["Type de contrat"]=="Assurance Vie"]
            st.subheader("💼 Souscripteurs avec un contrat 'Assurance Vie'")
            st.dataframe(sousc[["Numéro de contrat","Nom du souscripteur","Montant versé","Type de contrat","Banque / Compagnie"]])
            
         # Option pour filtrer les contrats "Contrat de Capitalisation"
        if st.sidebar.checkbox("🛡️  Afficher uniquement les souscripteurs avec un contrat 'Contrat de Capitalisation'",key="Capitalisation_checkbox"):
            sousc=DF[DF["Type de contrat"]=="Contrat de Capitalisation"]
            st.subheader("💼 Souscripteurs avec un contrat 'Contrat de Capitalisation'")
            st.dataframe(sousc[["Numéro de contrat","Nom du souscripteur","Montant versé","Type de contrat","Banque / Compagnie"]])

        
        # Si l'utilisateur clique sur le bouton pour générer le graphique des contrats par année
        if st.button("📈 Générer le graphique"):
            # Appel de la fonction pour créer le graphique et obtenir son chemin
            image_path = creer_graphique_contrats_par_annee(DF)
            # Affichage du graphique dans l'interface Streamlit
            st.image(image_path, caption="Contrats par année", use_container_width=True)
            st.success("✅ Graphique généré avec succès !")
            # Bouton pour générer le PDF (séparé)
        # Si l'utilisateur clique sur le bouton pour générer le rapport PDF
        if st.button("📑 Générer le rapport PDF"):
             # Appel de la fonction pour générer le PDF
            pdf_path = generer_pdf(DF)
            if pdf_path and os.path.exists(pdf_path):
                st.success("✅ Rapport PDF généré avec succès !")
                # Offrir un bouton de téléchargement du rapport PDF généré
                with open(pdf_path, "rb") as f:
                    st.download_button("📥 Télécharger le PDF", f, file_name="rapport_ficovie.pdf")
            else:
                st.error("❌ Échec de la génération du PDF.")
         # Si l'utilisateur clique sur le bouton pour générer le graphique des contrats par année       
        if st.button("📊 Répartition_des_types_de_contrat"):
            image_path=repartition_par_contrat(DF)
            if image_path:
                st.image(image_path,caption="Répartition_des_types_de_contrat",use_container_width=True)
                st.success(" ✅ Graphique généré avec succès ! ")
            else:
                st.error("❌ Erreur lors de la création du graphique.")

        # Si l'utilisateur clique sur le bouton pour générer le graphique des contrats par année       
        if st.button("📊 Répartition des montants par compagnie"):
            image_path=repartition_par_compagnie(DF)
            if image_path:
                st.image(image_path,caption="Répartition des montants par compagnie",use_container_width=True)
                st.success(" ✅ Graphique généré avec succès ! ")
            else:
                st.error("❌ Erreur lors de la création du graphique.")

        # 📌 Filtrer par compagnie d'assurance
        compagnies = DF["Banque / Compagnie"].unique()
        # Création du menu déroulant pour choisir une compagnie
        compagnie_selectionnee = st.sidebar.selectbox("🏦 Sélectionnez une compagnie d'assurance pour filtrer :", compagnies, key="compagnie_filter")
        # Filtrer les données selon la compagnie choisie
        donnees_filtrees = DF[DF["Banque / Compagnie"] == compagnie_selectionnee]
        # Affichage
        st.subheader(f"📋 Contrats pour la compagnie : {compagnie_selectionnee}")
        st.dataframe(donnees_filtrees[["Numéro de contrat", "Nom du souscripteur", "Type de contrat", "Montant versé"]])

        # Extraire les années uniques du fichier
        if "Annee" in DF.columns:
            annees = sorted(DF["Annee"].dropna().unique())
            annee_selectionnee = st.sidebar.multiselect("📅 Filtrer par année de souscription :", options=annees, default=annees)

            if annee_selectionnee:
                DF = DF[DF["Annee"].isin(annee_selectionnee)]
                st.subheader(f"📋 Données filtrées pour l'année(s) : {', '.join(map(str, annee_selectionnee))}")
                st.dataframe(DF[["Numéro de contrat", "Nom du souscripteur", "Type de contrat", "Montant versé", "Annee", "Banque / Compagnie"]])
            else:
                st.info("📌 Veuillez sélectionner au moins une année pour afficher les résultats.")
        else:
            st.warning("⚠️ La colonne 'Annee' n'existe pas dans votre fichier.")
        
        # Ajouter un champ de saisie pour filtrer par souscripteur
        souscripteur=st.text_input("✍️ Entrez le nom du souscripteur","")
        if souscripteur:
            resultat = DF[DF["Nom du souscripteur"].str.contains(souscripteur, case=False, na=False)]
            
            if not resultat.empty :
                st.subheader(f" 🏆 Résultats pour le souscripteur : {souscripteur}")
                st.dataframe(resultat[["Numéro de contrat", "Nom du souscripteur", "Montant versé", "Type de contrat", "Banque / Compagnie"]])
            else:
                st.warning("❌ Aucun souscripteur trouvé correspondant à ce nom.")
        
        # Ajouter un champ de saisie pour un montant spécifique
        montant_min = st.number_input("💶 Entrez le montant minimum", min_value=0.0, step=10.00)
        montant_max = st.number_input("💶 Entrez le montant maximum", min_value=0.0, step=010.00)
         # On applique le filtre sur les deux bornes
        if montant_min or montant_max:
            DF = DF[(DF["Montant versé"] >= montant_min) & (DF["Montant versé"] <= montant_max)]
            st.subheader(f"💰 Contrats avec un montant entre {montant_min}€ et {montant_max}€")
            st.dataframe(DF[["Numéro de contrat", "Nom du souscripteur", "Montant versé", "Type de contrat", "Banque / Compagnie"]])

        # Ajouter un champ pour sélectionner une date de souscription
        date_min=st.date_input("📅 Sélectionnez la date de souscription minimale",DT.date(2010,1,1))
        date_max=st.date_input("📅 Sélectionnez la date de souscription maximale",DT.date(2024,12,31))
        if date_min or date_max:
            DF["Date de souscription"] = pd.to_datetime(DF["Date de souscription"], errors='coerce')
            # Conversion de la colonne en datetime et application du filtre
            DF = DF[(DF["Date de souscription"] >= pd.to_datetime(date_min)) & (DF["Date de souscription"] <= pd.to_datetime(date_max))]
            st.subheader(f" 🎯 Contrats souscrits entre le {date_min} et le {date_max}")
            st.dataframe(DF[["Numéro de contrat", "Nom du souscripteur", "Montant versé", "Type de contrat", "Banque / Compagnie", "Date de souscription"]])



    except Exception as e:
        # Si une erreur se produit (par exemple, mauvaise lecture du fichier), afficher un message d'erreur
        st.error(f"❌ Erreur lors du traitement du fichier : {e}")
        
# Si aucun fichier n'est importé, afficher un message d'information
st.info(" 📂 Veuillez importer un fichier Excel pour commencer.")       




