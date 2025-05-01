# Reddit Modération

Une application web Django permettant de naviguer et modérer du contenu provenant de Reddit avec filtrage automatique des commentaires toxiques.

## 📋 Description

Reddit Modération est une application qui utilise l'API Reddit (PRAW) pour afficher les posts populaires et rechercher du contenu sur Reddit. L'application offre également une fonctionnalité de modération qui filtre automatiquement les commentaires contenant des mots toxiques ou inappropriés.

## ✨ Fonctionnalités

- **Page d'accueil** : Affiche les 10 posts les plus populaires ("hot") sur Reddit
- **Recherche** : Permet de rechercher des posts Reddit sur un sujet spécifique
- **Modération** : Affiche un post spécifique avec ses commentaires, en séparant les commentaires appropriés de ceux contenant des mots toxiques
- **Interface intuitive** : Design responsive avec Bootstrap pour une utilisation sur desktop et mobile
- **Fil d'Ariane** : Navigation claire avec un système de "breadcrumbs"

## 🔧 Prérequis techniques

- Python 3.x
- Django 3.x ou supérieur
- Module PRAW (Python Reddit API Wrapper)
- Compte développeur Reddit (pour obtenir client_id, client_secret et user_agent)

## 📦 Installation

1. Clonez ce dépôt :
```
git clone https://github.com/DaSilvaThomas/django-moderation.git
```

2. Installez les dépendances :
```
pip install -r requirements.txt
```

3. Configurez vos identifiants Reddit dans `views.py` :
```python
reddit = praw.Reddit(
    client_id="Votre_client_id",
    client_secret="Votre_client_secret",
    user_agent="Votre_user_agent"
)
```

4. Lancez le serveur de développement :
```
python manage.py migrate
python manage.py runserver
```

5. Accédez à l'application dans votre navigateur à l'adresse http://127.0.0.1:8000/accueil/

## 🚀 Utilisation

### Page d'accueil
- La page d'accueil affiche automatiquement les 10 posts les plus populaires de Reddit
- Chaque post affiche le subreddit, l'âge du post, le titre, l'image (si disponible), le nombre de votes et commentaires

### Recherche
- Utilisez la barre de recherche en haut pour trouver des posts sur un sujet spécifique
- Les résultats affichent les 10 posts les plus pertinents publiés durant la semaine précédente

### Modération
- Cliquez sur "Voir le post" pour accéder à la page de modération d'un post spécifique
- La page affiche d'abord les commentaires "propres" ne contenant pas de mots inappropriés
- Cliquez sur le bouton "Afficher les commentaires filtrés" pour voir les commentaires contenant des mots toxiques
- Les mots toxiques sont mis en évidence en rouge

## 📝 Liste des mots filtrés

L'application filtre automatiquement les commentaires contenant les mots suivants :
```
"idiot", "stupid", "dumb", "hate", "useless", "rage", "toxic", 
"attack", "crap", "trash", "sucks", "angry", "frustrated", "insult", 
"fight", "annoying", "loser", "fail", "bullshit", "moron", "bitch"
```

Vous pouvez modifier cette liste dans la fonction `moderation_view` du fichier `views.py`.

## 🏗️ Structure du projet

- **views.py** : Contient les fonctions de vue pour récupérer et traiter les données Reddit
- **templates/application/** :
  - **index.html** : Template de base avec en-tête, pied de page et structure commune
  - **accueil.html** : Affichage des posts populaires
  - **recherche.html** : Résultats de recherche
  - **moderation.html** : Page de modération avec commentaires filtrés
- **static/application/** :
  - **style.css** : Styles généraux
  - **posts.css** : Styles pour l'affichage des posts
  - **script.js** : JavaScript pour l'interaction (affichage/masquage des commentaires filtrés)

## 👨‍💻 Développé par

Thomas Da Silva - Université Paris 8 Vincennes - Saint-Denis
