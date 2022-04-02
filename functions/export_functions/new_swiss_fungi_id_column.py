import json
import queue
from threading import Thread
from typing import Tuple

import pandas as pd
import urllib3


def new_swiss_fungi_id_column(species: pd.DataFrame):
    http = urllib3.PoolManager()
    nb_workers = 16

    class Worker(Thread):
        def __init__(self, request_queue):
            Thread.__init__(self)
            self.queue = request_queue
            self.swissfungi = pd.DataFrame([], columns=["GBIF1", "SwissFungi", "SwissFungi Obs"])

        def run(self):
            while True:
                species_row = self.queue.get()
                if species_row == "":
                    break

                gbif_id_1 = species_row.GBIF1
                gbif_id_2 = species_row.GBIF2
                # Récupérer l'espèce GBIF
                dataset_key = "c0633ec5-19cd-4a58-b84c-ca55c2e7ae64"
                swiss_fungi_id, swiss_fungi_obs = get_swiss_fungi_id(http,
                                                                     "v1/occurrence/search?dataset_key=" + dataset_key +
                                                                     "&limit=1&taxon_key=", str(gbif_id_1),
                                                                     str(gbif_id_2))

                result = pd.DataFrame(
                    {"GBIF1": [gbif_id_1], "SwissFungi": [swiss_fungi_id], "SwissFungi Obs": [swiss_fungi_obs]})

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


def get_swiss_fungi_id(http: urllib3.PoolManager, url, query1, query2) -> Tuple[str | None, str | None]:
    try:
        api_url = "https://api.gbif.org/"
        response = http.request('GET', api_url + url + query1)
        gbif_match = json.loads(response.data.decode('utf-8'))
        nb_swiss_fungi_obs = gbif_match["count"]
        if nb_swiss_fungi_obs > 0:
            return gbif_match["results"][0]["taxonID"].replace("infospecies.ch:swissfungi:", ""), nb_swiss_fungi_obs

        if query1 != query2:
            response = http.request('GET', api_url + url + query2)
            gbif_match = json.loads(response.data.decode('utf-8'))
            nb_swiss_fungi_obs = gbif_match["count"]
            if nb_swiss_fungi_obs > 0:
                return gbif_match["results"][0]["taxonID"].replace("infospecies.ch:swissfungi:", ""), nb_swiss_fungi_obs
            else:
                return None, None
        else:
            return None, None
    except urllib3.exceptions.HTTPError as e:
        print(e)
        print('Problème de connexion. Etes-vous connecté à internet ?')
