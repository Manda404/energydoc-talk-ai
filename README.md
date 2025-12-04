# ⚡ EnergyDocTalk AI

**Assistant intelligent pour analyser, comprendre et interroger des documents PDF dans le domaine de l’énergie.**

EnergyDocTalk AI est une solution d’IA conçue pour transformer la manière dont les entreprises manipulent leurs documents techniques, contractuels et réglementaires liés à l’énergie. Grâce à une architecture moderne basée sur le RAG (Retrieval-Augmented Generation), l’application permet d’extraire le texte des PDFs, de le restructurer en informations exploitables, puis d’interroger ces documents de manière naturelle.

---

## 🎯 Objectif du projet

EnergyDocTalk AI a pour ambition de :

* **Automatiser la lecture** de documents PDF complexes (contrats énergétiques, rapports techniques, factures, audits, réglementations…)
* **Permettre une recherche intelligente** directement dans le contenu des documents
* **Répondre aux questions métier en langage naturel**
* **Accélérer l’analyse documentaire** dans les équipes énergie, conseil, finance ou gestion de contrats

Le projet facilite ainsi l’accès, la compréhension et l’exploitation de données documentaires souvent volumineuses et techniques.

---

## 🔍 Fonctionnement général

Le workflow complet d’EnergyDocTalk AI repose sur trois étapes principales :

### 1️⃣ Extraction intelligente du texte (RAM-only)

Les documents PDF sont chargés **en mémoire**, sans jamais être écrits sur disque.
Le module d’extraction basé sur **PyMuPDF (fitz)** analyse chaque page et récupère un texte propre et exploitable.

### 2️⃣ Découpage en unités d’information (Chunks)

Le texte extrait est ensuite découpé en segments cohérents (chunks) via des règles de segmentation adaptées aux documents techniques.
Chaque segment est enrichi de métadonnées :

* nom du document
* numéro de page
* source d’origine

### 3️⃣ Indexation et recherche augmentée (RAG)

Les chunks sont transformés en embeddings et insérés dans un Vector Store (Pinecone ou FAISS).
Lors d’une question utilisateur, le système :

1. repère les passages les plus pertinents
2. les envoie à un modèle de langage (LLM)
3. génère une réponse claire, fiable et contextualisée

---

## 🖥️ Interface utilisateur

EnergyDocTalk AI propose une interface **Streamlit**, simple et efficace :

* upload de plusieurs PDF
* ingestion directe en mémoire
* visualisation du contenu extrait
* interrogation intelligente des documents

Aucune donnée n’est persistée en local, ce qui rend l’outil **compatibles avec Streamlit Cloud** et adapté à un usage sécurisé.

---

## 🧠 Domaines d’utilisation

EnergyDocTalk AI peut être utilisé dans de nombreux cas :

* Analyse de **contrats énergétiques**
* Lecture automatisée de **rapports techniques**
* Extraction d’informations dans des **factures d’énergie**
* Consultation rapide de **documents réglementaires**
* Support aux équipes de conseil et audit énergétique

Il constitue une base solide pour créer des assistants intelligents dans les secteurs :

* Énergie & Environnement
* Bâtiment & Infrastructure
* Industrie
* Conseil en efficacité énergétique
* Gestion de projets techniques

---

## 🚀 Un projet modulaire et évolutif

EnergyDocTalk AI repose sur une architecture claire :

* extraction PDF
* découpage intelligent
* vectorisation
* recherche RAG
* interface utilisateur

Chaque module peut être amélioré ou remplacé indépendamment, facilitant :

* l’ajout de nouveaux formats (Word, images, OCR)
* l’optimisation des modèles
* l’intégration dans des pipelines internes
* le déploiement cloud

---