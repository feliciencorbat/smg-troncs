import json
import queue
from threading import Thread

import pandas as pd
import urllib3

from constants import Constants


def new_swiss_fungi_count_column(species: pd.DataFrame):
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

                swissfungi_id = species_row.SwissFungi

                # Récupérer le nombre d'observations
                if swissfungi_id is not None:
                    swiss_fungi_count = get_swiss_fungi_count(http, "species/observations/count/", str(swissfungi_id))

                    result = pd.DataFrame(
                        {"SwissFungi": [swissfungi_id], "SwissFungi Observations": [swiss_fungi_count]})

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

    species = species.join(swiss_fungi_df.set_index('SwissFungi'), on="SwissFungi")

    return species


def get_swiss_fungi_count(http: urllib3.PoolManager, url, query) -> str | None:
    try:
        api_url = "https://www.wsl.ch/map_fungi/rest/"
        response = http.request('GET', api_url + url + query)
        swissfungi_count = json.loads(response.data.decode('utf-8'))
        return swissfungi_count

    except urllib3.exceptions.HTTPError as e:
        print(e)
        print('Problème de connexion. Etes-vous connecté à internet ?')
