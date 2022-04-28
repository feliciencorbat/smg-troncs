# Statistiques Troncs SMG

## Fonctions <a id="fonctions"></a>

- créer un fichier Excel modifié à partir de la liste originale
- vérifier les synonymies, les erreurs, les incohérences, ... de la liste originale
- créer des distributions avec limite et graphes en tuyaux d'orgue
- créer une matrice V Cramer (variables qualitatives)
- créer des tests Chi-2 avec graphes heatmap et camembert (variables qualitatives)
- créer des tests ANOVA avec graphes boîtes à moustaches (variable qualitative et quantitative)
- créer des graphes d'évolution des espèces

## Site web

https://troncs.champis.net

## Installation en local

- installer docker
- dans le dossier **website**, ajouter un fichier **.env** avec les variables:

      SECRET_KEY=... (générer avec https://djecrety.ir)
      DEBUG=True

- lancer la commande:

      docker-compose up -d --build

- dans la console du container troncs, lancer la commande:

      python manage.py migrate

- toujours dans cette console, créer un utilisateur avec la commande:

      python manage.py createsuperuser

- se connecter sur le site en local
- mettre à jour les données via le menu Données -> Mettre à jour les données