import json
import queue
from threading import Thread
import pandas as pd
import urllib3

from constants import Constants


def new_swiss_fungi_lr_column(species: pd.DataFrame):
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

                swiss_fungi_id = species_row.SwissFungi
                # Récupérer l'espèce SwissFungi
                swiss_fungi_lr = get_swiss_fungi_lr(http, str(swiss_fungi_id))

                result = pd.DataFrame(
                    {"SwissFungi": [swiss_fungi_id], "SwissFungi LR": [swiss_fungi_lr]})

                self.swissfungi = pd.concat([self.swissfungi, result])
                self.queue.task_done()

    # Création de la queue
    q = queue.Queue()

    for row in species.itertuples():
        if row.SwissFungi is not None:
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

    # Eliminer les duplicatas
    species = species.drop_duplicates()

    return species


def get_swiss_fungi_lr(http: urllib3.PoolManager, swiss_fungi_id: str) -> str | None:
    try:
        response = http.request('GET', "https://www.wsl.ch/map_fungi/rest/species/protectionFungus/" + swiss_fungi_id)
        swissfungi = json.loads(response.data.decode('utf-8'))
        if len(swissfungi) > 0:
            if swissfungi[0]["listCode"] == 2:
                return swissfungi[0]["endangeredAbbreviation"]
            else:
                return None
        else:
            return None
    except urllib3.exceptions.HTTPError as e:
        print(e)
        print('Problème de connexion. Etes-vous connecté à internet ?')
