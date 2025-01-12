import json
import queue
import difflib
from threading import Thread

import pandas as pd
import urllib3

from constants import Constants


def new_swiss_fungi_id_column(species: pd.DataFrame):
    http = urllib3.PoolManager()
    nb_workers = Constants.nb_workers

    class Worker(Thread):
        def __init__(self, request_queue):
            Thread.__init__(self)
            self.queue = request_queue
            self.swissfungi = pd.DataFrame([], )

        def run(self):
            while True:
                species_row = self.queue.get()
                if species_row == "":
                    break

                species = species_row.Espèce
                current_species = species_row[6]
                gbif1_id = species_row.GBIF1

                # Récupérer l'espèce SwissFungi
                swiss_fungi_id = get_swiss_fungi_id(http, "species/byName/", str(species), str(current_species))

                result = pd.DataFrame(
                    {"GBIF1": [gbif1_id], "SwissFungi": [swiss_fungi_id]})

                self.swissfungi = pd.concat([self.swissfungi, result])
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
    swiss_fungi_df = pd.DataFrame([], )
    for worker in workers:
        swiss_fungi_df = pd.concat([swiss_fungi_df, worker.swissfungi])

    species = species.join(swiss_fungi_df.set_index('GBIF1'), on="GBIF1")

    return species


def get_swiss_fungi_id(http: urllib3.PoolManager, url, query1, query2) -> str | None:
    try:
        api_url = "https://www.wsl.ch/map_fungi/rest/"

        response = http.request('GET', api_url + url + query1)
        swissfungi_match = json.loads(response.data.decode('utf-8'))
        if len(swissfungi_match) > 0:
            similarities = [
                (entry["taxonId"], difflib.SequenceMatcher(None, query1, entry["taxonName"]).ratio())
                for entry in swissfungi_match
            ]

            closest_match = max(similarities, key=lambda x: x[1])
            return closest_match[0]

        if query1 != query2:
            response = http.request('GET', api_url + url + query2)
            swissfungi_match = json.loads(response.data.decode('utf-8'))
            if len(swissfungi_match) > 0:
                return swissfungi_match[0]["taxonId"]

        return None

    except urllib3.exceptions.HTTPError as e:
        print(e)
        print('Problème de connexion. Etes-vous connecté à internet ?')
