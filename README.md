# P8 Creez une plateforme pour amateurs de Nutella
[![](https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQeH7711sJeOaZ_HOpwi3M7MjPOQeOPE2TyMxn-_NyxyHu_O2tm&s)](https://openclassrooms.com/fr)
[![](Pure_Beurre/substitute/static/substitute/png/biscuit.png)](biscuit.png)  

## Introduction 

    La startup Pur Beurre, avec laquelle vous avez déjà travaillé,  
    souhaite développer une plateforme web à destination de ses clients.  
    Ce site permettra à quiconque de trouver un substitut sain à un aliment  
    considéré comme "Trop gras, trop sucré, trop salé"  
    
## Cahier des charges 
Le cahier des charges est disponible en cliquant sur [ce lien](Pure_Beurre/substitute/static/substitute/pdf/Cahier_des_charges.pdf)  

## Fonctionnalités et Contraintes
Voici la liste des fonctionnalités :  
    
    - Affichage du champ de recherche dès la page d’accueil
    - La recherche ne doit pas s’effectuer en AJAX
    - Interface responsive
    - Authentification de l’utilisateur : création de compte en entrant un mail et un mot de passe, sans possibilité de changer son mot de passe pour le moment.
 
Voici la liste des contraintes majeures :  

    - Utilisez une base de données PostgreSql.
    - Incluez une page “Mentions Légales” qui contiendra les coordonnées de l’hébergeur ainsi que les auteurs des différentes ressources libres utilisées (template, photos, icônes, …).

## Conception
Le projet est conçu et réalisé selon une méthodologie agile.  
Il se compose de deux parties principales :  

    - Le Front-End
    - Le Back-End

Toutes les étapes du projet sont disponibles sur ce [Trello](https://trello.com/invite/b/YnrxAILd/7a2d98453860a05769cb8752e302cc2f/p8creezuneplateformepouramateursdenutella)

La conception du présent projet s'appuie sur [le cahier des charges](Pure_Beurre/substitute/static/substitute/pdf/Cahier_des_charges.pdf) fournie par la startup Pur Beurre.  
Elle reprend et respect le parcours utilisateur souhaité, tant au niveau de la navigation au sein du site, qu'au visuel proposé par chacune des pages web.  

### Base de données  
Ce site web contient sa propre base de données intégrant trois types de données :

    - Les données des produits
    - Les données des utilisateurs
    - Les données de texte

Conformément au cahier des charges, les données des produits sont collectées auprès des serveurs [OpenFoodFacts](https://fr.openfoodfacts.org).  
Ce sont des données purement descriptives (images, ingrédients, qualité nutritive).  
Les données utilisateurs reprennent les informations utiles à la création et à la connexion d'espace personnel (identifiant, adresse email, mot de passe).  
Enfin, les données de texte sont purement et simplement des phrases à afficher sur certaine page web (accueuil, mentions légales).  
Leur conservation en base de données permettent de mettre à jour plus facilement le contenu textuel de ces pages web.  

### Algorithme  
La fonctionnalité principale de ce site web est de proposer un aliment de substitution à l'utilisateur.  
Pour ce faire, un algorithme s'applique sur la base de données du site web afin de réaliser cette tâche.  
L'algorithme en question s'appuie sur trois critères précis :  

    - La saisie utilisateur
    - La categorie des produits 
    - Le nutriscore des produits

Une fois la saisie utilisateur validée, l'algorithme capture et analyse le texte, afin de vérifier si cette saisie est bien correcte.
Par la suite, il parcours la base de données du site web et remonte les produits directement concernés par la recherche.
Dans un second temps, il parcours à nouveau la base de données et remonte les produits indirectement concernés.  
Il procède en utilisant, non plus avec la saisie utilisateur, mais avec la catégorie de cette saisie.
Enfin, l'algorithme termine son traitement par un trie des produits trouvés sur la base du nutriscore.  
Voici un exemple du processus algorithmique :

    - L'utilisateur saisie : chocolat
    - les produits directs trouvés sont : biscuit lait chocolat, muesli avoine chocolat, glace chocolat
    - Les produits indirects trouvés sont : nesquick nestlé, savane tout choco brossard, kinder country 

Dans cet exemple, les produits directs contiennent tous le mot "chocolat" dans leur appélation, ce qui coresspond directement à la recherche de l'utilisateur.
Les produits indirects ne contiennent pas le mot "chocolat" dans leur appélation mais plutôt dans leur catégorie respective. Ils sont donc tout autant concernés par cette recherche.  

### Front-End  
La conception de la partie visuel du site se découpe dans les 9 parties suivantes (User-Story):  

    - A10_PageAccueil
    - A16_CorpsAccueil
    - A20_PageResultats
    - A30_PageAliment
    - A40_PageMonCompte
    - A41_CreerCompte
    - A42_SeConnecter
    - A43_Historique
    - EX1_TestsFrontEnd

Ses parties reprennent les élements du cahier des charges en termes de "zoning", de code couleurs, polices et images.
Elles y intègrent aussi quelques opérations intelligentes de faible profondeur, tel que la création d'espaces personnels ou  
l'authentification des utilisateurs. Cependant, ses opérations sont vite déléqués à la partie Back-end. 
 
### Back-End  
La conception de la partie intelligente du site se découpe dans les 9 parties suivantes (User-Story):

    - B10_EspacePersonnel
    - B11_Authentification
    - B12_CreerCompte
    - B13_SeConnecter
    - B20_MoteurRecherche
    - B21_ApiOpenfoodfacts
    - B22_BaseDeDonnées
    - B30_EnregistrementProduit
    - EX2_TestsBackEnd

Ces parties reprennent les étapes du processus algorithmique, remplissant donc la fonctionnalité principale du projet.  
### Conformité
Cette partie de la conception, la conformité, prend tout son sens à la fin du projet.  
Elle énumère les composants essentiels au bon fonctionnement du site et à sa compréhension.  

    - CX3_Déploiement
    - DX1_Documentation
    - DX2_Qualité

Le déploiement est l'étape finale de la production du site web.
La documentation reprend les informations descriptives du projet et de son évolution.
La qualité définie la clarté de rédaction du code.    

## Réalisation
La réalisation reprend les "users-story" de la conception.  
Cependant, elles n'ont pas toutes été réalisées dans cet ordre.  

Globalement, la réalisation à suivi un cursus de 6 étapes, ou chaque étapes contient une ou plusieurs "user-story".  

    - Initialisation du Projet Django
    - Création de la page d'accueil
    - Création des pages comptes et authentification
    - Création des fonctionnalités d'intégration, de recherche et d'affichage de produits
    - Création des fonctionnalités de sauvegarde et d'affichage des substituts
    - Déploiement du site web
    
## Production
La production contient majoritairement l'étape du déploiement du site Web.  
Cependant, une mise en conformité a été mise en oeuvre pour respecter l'architecture du serveur hébergeur.  
Cette mise en conformité agit sur certains traits du site web tel que l'emplacement des fichiers "static", ou encore,  
les chemins d'accès au fichiers internes. 

    
### Installation  
Suite à l'hébergement du site web chez [DigitalOcean](https://www.digitalocean.com), le projet doit encore suivre une dernière étape avant d'être totalement opérationnel.
La base de données du site web est encore vide auprès de l'hébergeur. Une commande spéciale doit être lancée afin de remplir, ou mettre à jour la base.
Enfin les services web peuvent démarrer pour rendre le site web accessible (NGINX, GUNICORN).

### Utilisation  
L'utilisation du site [Pur Beurre](http://206.189.30.229/substitute/) est très simple.  
Sans s'authentifier, vous pouvez faire des recherches de produits et consuler leurs informations descriptives.  
En vous authentifiant, vous pouvez aller plus loin et sauvegarder les produits souhaités.  
Vous les retrouverez dans l'espace dédiés à vos aliments sauvegardés. 
Voici ci-dessous le parcours classique d'un utilisateur non-authentifié:  

    - Se rendre sur le site.  
    - Cliquer sur l'icone de connexion dans le coin supérieur droit (image d'avatar noire).  
    - Cliquer sur "créer mon compte" (boutton orange).  
    - Renseigner Nom d'utilisateur (identifiant), Adresse électronique, Mot de passe.  
    - Cliquer sur création de compte (boutton orange).  
    - Après avoir été redirigé vers la page de connexion, saisir le Nom d'utilisateur, le Mot de passe puis cliquer sur "Se connecter" (botton or).  
    - Après avoir été redirigé vers la page de connexion, saisir dans la barre de recherche le produit souhaité.  
    - Une liste de produits est affichée. Cliquer sur le nom du substitut souhaité.  
    - Après avoir été redirigé vers la page de description du substitut, cliquer sur sauvegarder au niveau inférieur de l'écran.    
    - La sauvegarde du substitut a été réalisé. Cliquer sur la carotte pour afficher l'ensenmble des substituts sauvegardés.  
    - Une fois la navigation terminée, cliquer sur le boutton de déconnexion dans le coin supérieur droit de l'écran.  
    - Vous pouvez quitter le site "Pur Beurre".   
       

## Versions  

    - Langage programmation : Python 3.8
    - Framework : Django 3.1.2
    - Base de données : PostgreSql 13
    - Serveur web wsgi : Gunicorn 20.0.4
    - Tests unitaires : Django.Testcase & Django.SimpleTestCase
    - Tests fonctionnels dynamiques : Selenium 3.141
    - Hébergeur : DigitalOcean
    
    - Site Web : Pur Beurre 1.1
    
    

## Rappel des liens  

[Pur Beurre](http://206.189.30.229/substitute/)  
[DigitalOcean](https://www.digitalocean.com)  
[OpenFoodFacts](https://fr.openfoodfacts.org)  
[Trello](https://trello.com/invite/b/YnrxAILd/7a2d98453860a05769cb8752e302cc2f/p8creezuneplateformepouramateursdenutella)    
[GitHub](https://github.com/StephenAOGOLO/P8_Creez_une_plateforme_pour_amateurs_de_Nutella.git)    

## Auteur  
Stephen A.OGOLO

## Remerciements  
Merci pour cette lecture et pour l'attention portée à ces informations.  
Bonne utilisation ;)  
