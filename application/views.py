from django.shortcuts import render
import praw  # Module python pour utiliser l'API Reddit
import time
import re  # Pour split une chaîne de caractère


# Authentification API Reddit
reddit = praw.Reddit(
    client_id="Votre_client_id",
    client_secret="Votre_client_secret",
    user_agent="Votre_user_agent"
)


def accueil_view(request):
    posts = []
    resultats = reddit.subreddit("all").hot(limit=10)  # Recherche des 10 subreddits les plus "hot"

    for resultat in resultats:
        # Calcul du temps écoulé depuis la publication d'un post reddit
        temps_creation = resultat.created_utc
        temps_ecoule = time.time() - temps_creation  # time.time() => temps actuel

        if temps_ecoule < 3600:
            age = f"il y a {int(temps_ecoule // 60)} m"
        elif temps_ecoule < 86400:
            age = f"il y a {int(temps_ecoule // 3600)} h"
        else:
            age = f"il y a {int(temps_ecoule // 86400)} j"

        # On récupère l'image du post reddit en bonne qualité
        image = None
        if hasattr(resultat, "preview") and "images" in resultat.preview:
            image = resultat.preview['images'][0]['source']['url'].replace("&amp;", "&")

        # Stockage des caractéristiques des posts sous forme d'objets
        posts.append({
            "titre": resultat.title,
            "score": resultat.score,
            "commentaires": resultat.num_comments,
            "subreddit": resultat.subreddit.display_name,
            "subreddit_icon": resultat.subreddit.icon_img or "",
            "age": age,
            "image": image,
            "post_id": resultat.id,
        })

    return render(request, 'application/accueil.html', {
        'posts': posts,
        'breadcrumbs': [("Vous êtes ici : Accueil", "/accueil/")]  # Breadcrumbs pour la page d'accueil
    })


def recherche_view(request):
    posts = []
    recherche = request.GET.get('search', '')  # On récupère la recherche de l'utilisateur

    if recherche:
        resultats = reddit.subreddit("all").search(recherche, sort="hot", time_filter="week", limit=10)

        for resultat in resultats:
            # Calcul du temps écoulé depuis la publication d'un post reddit
            temps_creation = resultat.created_utc
            temps_ecoule = time.time() - temps_creation  # time.time() => temps actuel

            if temps_ecoule < 3600:
                age = f"il y a {int(temps_ecoule // 60)} m"
            elif temps_ecoule < 86400:
                age = f"il y a {int(temps_ecoule // 3600)} h"
            else:
                age = f"il y a {int(temps_ecoule // 86400)} j"

            # On récupère l'image du post reddit en bonne qualité
            image = None
            if hasattr(resultat, "preview") and "images" in resultat.preview:
                image = resultat.preview['images'][0]['source']['url'].replace("&amp;", "&")

            posts.append({
                "titre": resultat.title,
                "score": resultat.score,
                "commentaires": resultat.num_comments,
                "subreddit": resultat.subreddit.display_name,
                "subreddit_icon": resultat.subreddit.icon_img or "",
                "age": age,
                "image": image,
                "post_id": resultat.id,
            })

    return render(request, 'application/recherche.html', {
        'recherche': recherche,
        'posts': posts,
        'breadcrumbs': [
            ("Vous êtes ici : Accueil", "/accueil/"),
            ("Recherche", "/recherche/")
        ]
    })


def moderation_view(request):
    # Liste de mots à filtrés
    stopwords = [
        "idiot", "stupid", "dumb", "hate", "useless", "rage", "toxic", 
        "attack", "crap", "trash", "sucks", "angry", "frustrated", "insult", 
        "fight", "annoying", "loser", "fail", "bullshit", "moron", "bitch"
    ]

    post_id = request.GET.get('id')  # On récupère l'id du post
    age_post = request.GET.get('age')  # On récupère l'age du post
    image = request.GET.get('img')  # On récupère l'image du post

    resultat = reddit.submission(id=post_id)  # On récupère les informations du post
    resultat.comment_sort = 'top'

    commentaires_clean = []
    commentaires_filtres = []

    for commentaire in resultat.comments.list()[:20]:
        commentaire_body = commentaire.body  # On récupère le contenu du commentaire
        commentaire_body_lower = commentaire_body.lower()

        # Si un stopword est présent dans le commentaire, on l'ajoute au tableau "mots_filtrés"
        mots_filtrés = []
        for mot in stopwords:
            if mot in commentaire_body_lower:
                mots_filtrés.append(mot)

        # Découpage des commentaires en liste de mot sans ponctuation
        mots = re.findall(r'\b\w+\b', commentaire_body_lower)

        # Stockage des mots à mettre en rouge dans les commentaires filtrés
        mots_rouge = []
        for mot in mots:
            for stopword in stopwords:
                if mot.startswith(stopword):
                    mots_rouge.append(mot)
        
        # Calcul de l'âge du commentaire
        temps_creation_commentaire = commentaire.created_utc
        temps_ecoule_commentaire = time.time() - temps_creation_commentaire

        if temps_ecoule_commentaire < 3600:
            age_commentaire = f"il y a {int(temps_ecoule_commentaire // 60)} m"
        elif temps_ecoule_commentaire < 86400:
            age_commentaire = f"il y a {int(temps_ecoule_commentaire // 3600)} h"
        else:
            age_commentaire = f"il y a {int(temps_ecoule_commentaire // 86400)} j"

        commentaire_data = {
            "auteur": str(commentaire.author),
            "score": commentaire.score,
            "body": commentaire.body,
            "auteur_icon": commentaire.author.icon_img or "",
            "age": age_commentaire,
            "mots": mots,
            "mots_rouge": mots_rouge,
        }

        # On sépare les commentaires filtrés et clean
        if mots_filtrés:
            commentaires_filtres.append(commentaire_data)
        else:
            commentaires_clean.append(commentaire_data)
        
    post = {
        "titre": resultat.title,
        "score": resultat.score,
        "nb_commentaires_clean": len(commentaires_clean),
        "nb_commentaires_filtres": len(commentaires_filtres),
        "subreddit": resultat.subreddit.display_name,
        "subreddit_icon": resultat.subreddit.icon_img or "",
        "age": age_post,
        "image": image,
        "body": resultat.selftext,      
    }

    return render(request, 'application/moderation.html', {
        'post': post,
        'commentaires_clean': commentaires_clean,
        'commentaires_filtres': commentaires_filtres,
        'breadcrumbs': [
            ("Vous êtes ici : Accueil", "/accueil/"),
            ("Modération", "/modération/")
        ]
    })
