import urllib3
import json
from typing import Tuple
from threading import Thread
import queue
import pandas as pd
from classes.species import Species
from constants import Constants


def new_gbif_columns(species: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    http = urllib3.PoolManager()
    nb_workers = 16

    class Worker(Thread):
        def __init__(self, request_queue):
            Thread.__init__(self)
            self.queue = request_queue
            self.species = pd.DataFrame([], columns=["Espèce", "Espèce actuelle", "Phylum", "Ordre", "GBIF1", "GBIF2"])
            self.errors = pd.DataFrame([], )

        def run(self):
            while True:
                species_row = self.queue.get()
                if species_row == "":
                    break

                species_name = species_row.Espèce
                # Récupérer l'espèce GBIF
                gbif_species = get_gbif_species(http, "v1/species/match?kingdom=Fungi&name=", species_name)
                old_gbif_id = gbif_species.key

                # Vérifier l'orthographe des noms d'espèces
                writing_errors_rows = writing_errors(species_name, gbif_species)
                self.errors = pd.concat([self.errors, writing_errors_rows])

                # Si l'espèce n'est pas acceptée et n'est pas dans la liste des erreurs de synonymes, changer l'espèce
                if (gbif_species.status != "ACCEPTED") & (gbif_species.species not in Constants.gbif_synonyms_errors):
                    gbif_species = get_gbif_species(http, "v1/species/", str(gbif_species.accepted_key))
                    print("Nom GBIF pour " + species_name + ": " + gbif_species.species)

                if gbif_species.rank == "SPECIES" or gbif_species.rank == "VARIETY" or \
                        gbif_species.rank == "SUBSPECIES" or gbif_species.rank == "FORM":
                    result = pd.DataFrame({"Espèce": [species_name], "Espèce actuelle": [gbif_species.species],
                                           "Phylum": [gbif_species.phylum], "Ordre": [gbif_species.order],
                                           "GBIF1": [old_gbif_id], "GBIF2": [gbif_species.key]})
                    self.species = pd.concat([self.species, result])
                else:
                    print("!!! " + species_name + " non récupérée par GBIF")
                    error_row = pd.DataFrame({'Ligne': [row.Index + 2], 'Espèce': [species_name],
                                              "Type d'erreur": ["L'espèce n'a pas été trouvée par GBIF"]})
                    self.errors = pd.concat([self.errors, error_row])

                self.queue.task_done()

    # Création de la queue
    q = queue.Queue()

    for row in species.itertuples():
        # Ajouter les lignes à la queue
        q.put(row)

    # Les workers fonctionnent jusqu'à ce qu'ils aient un texte vide
    for _ in range(nb_workers):
        q.put("")

    # Créer les workers
    workers = []
    for _ in range(nb_workers):
        worker = Worker(q)
        worker.start()
        workers.append(worker)
    # Joindre les workers
    for worker in workers:
        worker.join()

    # Combiner les résultats de tous les workers
    gbif_secies_df = pd.DataFrame([], )
    errors = pd.DataFrame([], )
    for worker in workers:
        gbif_secies_df = pd.concat([gbif_secies_df, worker.species])
        errors = pd.concat([errors, worker.errors])

    species = species.join(gbif_secies_df.set_index('Espèce'), on="Espèce")

    return species, errors


def get_gbif_species(http: urllib3.PoolManager, url: str, query: str) -> Species:
    try:
        api_url = "https://api.gbif.org/"
        response = http.request('GET', api_url + url + query)
        gbif_match = json.loads(response.data.decode('utf-8'))
        return Species(gbif_match["canonicalName"],
                       gbif_match["phylum"] if "phylum" in gbif_match else None,
                       gbif_match["order"] if "order" in gbif_match else None,
                       gbif_match["rank"],
                       gbif_match["taxonomicStatus"] if "taxonomicStatus" in gbif_match else gbif_match["status"],
                       gbif_match["key"] if "key" in gbif_match else gbif_match["usageKey"],
                       gbif_match["acceptedUsageKey"] if "acceptedUsageKey" in gbif_match else None)
    except urllib3.exceptions.HTTPError as e:
        print(e)
        print('Problème de connexion. Etes-vous connecté à internet ?')
        exit()


def writing_errors(species_name: str, gbif_species: Species) -> pd.DataFrame:
    errors = pd.DataFrame([], )
    # Tester si l'orthographe est bonne sauf pour quelques espèces
    if species_name not in Constants.default_species_writing:
        if species_name != gbif_species.species:
            print("!!! Orthographe douteuse pour " + species_name + ", peut-être plutôt: " + gbif_species.species)
            error_row = pd.DataFrame({'Ligne': [""], 'Espèce': [species_name],
                                      "Type d'erreur": [
                                          "Orthographe douteuse, peut-être plutôt: " + gbif_species.species]})
            errors = pd.concat([errors, error_row], ignore_index=True, axis=0)

    return errors
