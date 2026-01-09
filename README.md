
---

# Système de Gestion des Congés (Python/POO)

Ce projet est une application de gestion des congés réalisée en Python, illustrant les concepts de la Programmation Orientée Objet (POO) et la persistance de données avec SQLite.

## Architecture du Projet

L'application suit une architecture multicouche pour assurer la séparation des responsabilités :

* **Models** : Définition des entités métier (Héritage, Polymorphisme).
* **DAO (Data Access Object)** : Gestion exclusive des requêtes SQL.
* **Services** : Logique métier et contrôle des règles d'entreprise.
* **UI (CustomTkinter)** : Interface graphique moderne et réactive.

---

## Guide d'exécution

### 1. Installation des dépendances

Le projet utilise `customtkinter` pour une interface graphique moderne. Assurez-vous de l'installer via pip :

```bash
pip install customtkinter

```

### 2. Initialisation de la base de données

Vous n'avez pas besoin de créer manuellement le fichier `conges.db`.

* Au premier lancement du script principal, le système vérifie l'existence du dossier `data/`.
* Il initialise automatiquement la base de données et crée les tables nécessaires (`employes` et `demandes_conge`).

### 3. Lancer l'application

Pour démarrer le système, exécutez le fichier à la racine du projet :

```bash
python main.py

```

---

## Scénario de test minimal (Démo)

Pour prouver le bon fonctionnement des règles métier et du polymorphisme, suivez ces étapes avec les données pré-chargées :

### Étape 1 : Connexion Employé

1. Lancez l'application.
2. Connectez-vous avec le matricule : **`E001`** (Ali Dupont).
3. **Observation** : Son solde est de **22 jours**.
4. Allez dans "Poser un congé" et soumettez une demande de type **Annuel** du `2026-06-01` au `2026-06-05` (5 jours).
5. Déconnectez-vous.

### Étape 2 : Validation Responsable RH

1. Connectez-vous avec le matricule : **`R001`** (Hicham Zili).
2. Allez dans le menu **"Valider les demandes"**.
3. Cliquez sur le bouton **✔ (Accepter)** pour la demande d'Ali Dupont.
4. Déconnectez-vous.

### Étape 3 : Vérification du solde (Polymorphisme)

1. Reconnectez-vous avec le matricule : **`E001`**.
2. **Observation** : Le solde a été automatiquement mis à jour. Il affiche désormais **17 jours** (22 - 5).
3. Allez dans "Mes demandes" : le statut est passé à **"Accepté"**.

---

## Structure des fichiers

```text
.
├── main.py                 # Point d'entrée de l'application
├── data/                   # Contient la base SQLite (conges.db)
├── dao/                    # Couche d'accès aux données (SQL)
├── models/                 # Classes métier et constantes (Enum)
├── services/               # Logique métier et Authentification
└── ui/                     # Code de l'interface graphique

```

---