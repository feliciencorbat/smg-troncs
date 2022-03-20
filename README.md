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

![](readme/21.png)

- Il faut cliquer sur l'onglet "Python Packages"
- Dans le champ de recherche, écrire "pip-tools"
- Sélectionner la librairie "pip-tools"
- Cliquer sur le bouton Install

![](readme/22.png)

- Cliquer sur le bouton main
- Cliquer sur "Edit Configurations"

![](readme/23.png)

- Cliquer sur le bouton +
- Cliquer sur "Shell Script"

![](readme/27.png)

- Dans le champ "Name", donner un nom comme par exemple "update"
- Dans le champ "Script path:", il faut sélectionner le fichier "update.sh"
- Cliquer OK

Pour ajouter les librairies, les infos sont ci-dessous: [Récupérer les dernières mises à jour](#miseajour)

## Utilisation <a id="utilisation"></a>

### Lancer l'application <a id="lancer"></a>

Il suffit de cliquer sur le triangle vert.

![](readme/17.png)

### Récupérer les dernières mises à jour (fichiers et librairies) <a id="miseajour"></a>

Il faut au préalable avoir ajouté [les librariries](#librairies)

Cela récupère les derniers fichiers modifiés ou ajoutés. 
Il permet aussi d'ajouter et mettre à jour les libraries.

![](readme/19.png)

Par exemple, lors de l'utilisation de l'application, une erreur avec le message: 
"ModuleNotFoundError: No module named 'nom_module' apparaît. 
Cela signifie qu'une libraririe est manquante.

![](readme/26.png)

- Sélectionner "update"
- Cliquer sur le triangle vert
- Les fichiers et les librairies seront mis à jour