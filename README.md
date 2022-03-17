# Statistiques Troncs SMG

## Sommaire
- [Fonctions](#fonctions)
- [Installation](#installation) 
  - [Installer Python](#installerpython)
  - [Installer PyCharm](#installerpycharm)
  - [Ajouter le dépôt Github à PyCharm](#ajoutergithub)
  - [Lier Python au projet](#lierpython)
  - [Indiquer où se trouve le fichier de lancement](#lancement)
  - [Ajouter les librairies](#librairies)
- [Utilisation](#utilisation)
  - [Lancer l'application](#lancer)
  - [Récupérer les dernières mises à jour](#miseajour)
  - [Une libraire est manquante](#librairie)

## Fonctions <a id="fonctions"></a>

- créer un fichier Excel modifié à partir de la liste originale
- vérifier les synonymies, les erreurs, les incohérences, ... de la liste originale
- créer des distributions avec limite et affichage en tuyaux d'orgue
- créer des tests Chi-2 avec affichage en heatmap
- créer des graphes d'évolution des espèces

## Installation <a id="installation"></a>

### Installer Python <a id="installerpython"></a>

Télécharger et installer Python à l'adresse: https://www.python.org/downloads/

![](readme/0.png)

Ne pas oublier de cocher "Add Python 3.x to PATH"

### Installer PyCharm <a id="installerpycharm"></a>

Télécharger et installer PyCharm à l'adresse: https://www.jetbrains.com/fr-fr/pycharm/download/

Il faut choisir la version Community (gratuite et open source)

### Ajouter le dépôt Github à PyCharm <a id="ajoutergithub"></a>

Au lancement de PyCharm, vous obtenez cette fenêtre:

(si cette fenêtre n'est pas affichée, choisir le menu "Git" -> "Clone...")

![](readme/1.png)

Cliquer le bouton "Get from VCS"

![](readme/2.png)

Si Git n'est pas installé, cliquer "Download and Install"

![](readme/3.png)

Dans le champ URL, ajouter: https://github.com/feliciencorbat/smg-troncs.git

Dans le champ Directory, choisir où ajouter les fichiers (par exemple dans le dossier Documents)

Enfin, cliquer sur "Clone"

![](readme/4.png)

Tous les fichiers du projet sont ajoutés au dossier et affichés dans PyCharm

### Lier Python au projet <a id="lierpython"></a>

![](readme/5.png)

Sur le bouton "IDE and Project Settings", sélectionner "Preferences..."

![](readme/6.png)

Se rendre sur "Project: smg-troncs" -> "Python Interpreter"

Cliquer sur le bouton "Settings" et choisir "Add..."

![](readme/7.png)

Sélectionner "Virtualenv Environment"

Dans "Location", choisir le lieu où se trouvera l'environnement virtuel
Laisser par défaut dans le dossier du projet

Cliquer "OK"

![](readme/8.png)

Votre environnement virtuel avec Python est installé.

### Indiquer où se trouve le fichier de lancement <a id="lancement"></a>

![](readme/9.png)

Cliquer sur le bouton "Add Configuration..."

![](readme/11.png)

Cliquer sur "+" et choisir "Python"

![](readme/12.png)

Dans le champ "Script path:", sélectionner le fichier "main.py" de votre projet

![](readme/13.png)

Dans le champ "Python interpreter:", l'interpréteur Python créé précédemment devrait automatiquement être ajouté, sinon le sélectionner.

Cliquer "OK"

### Ajouter les librairies <a id="librairies"></a>

![](readme/14.png)

En lançant l'application en cliquant sur le triangle vert "Run 'main'", des erreurs seront affichées car des librairies manquent. Dans le message en rouge, il est indiqué qu'il manque le module 'pandas'.

![](readme/15.png)

Une solution pour installer les librairies est d'aller dans l'onglet "Python Packages".
Dans le champ "Search for more packages", écrire "pandas"
Sélectionner "pandas" et cliquer sur le bouton "Install".

Il faut réaliser l'opération jusqu'à ce que toutes les librairies soient installées.

![](readme/16.png)

L'autre solution est de naviguer dans les fichiers (le dossier "functions" en particulier). Une fois que le projet est indexé (ce qui peut prendre un peu de temps) par PyCharm, les librairies non installées sont surlignée en rouge. En les survolant, il est proposé de les installer ("install package matplotlib" par exemple).

## Utilisation <a id="utilisation"></a>

### Lancer l'application <a id="lancer"></a>

Il suffit de cliquer sur le triangle vert.

![](readme/17.png)

### Récupérer les dernières mises à jour <a id="miseajour"></a>

Cliquer sur la "Flèche bleue Update Project..." et cliquer OK.

![](readme/18.png)

### Une libraire est manquante <a id="librairie"></a>

![](readme/19.png)

Lors de l'utilisation de l'application, une erreur avec le message: 
"ModuleNotFoundError: No module named 'nom_module' apparaît.

![](readme/20.png)

- Il faut cliquer sur l'onglet "Python Packages"
- Dans le champ de recherche, écrire le nom de la librairie manquante
- Cliquer sur le bouton Install