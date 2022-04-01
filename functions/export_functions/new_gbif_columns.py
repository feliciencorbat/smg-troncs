import urllib.request
import urllib.error
import json
from typing import Tuple

import pandas as pd

from classes.species import Species
from constants import Constants


def new_gbif_columns(species: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    errors = pd.DataFrame([], )

    for row in species.itertuples():
        species_name = row.Espèce
        print(species_name)

        gbif_species = get_gbif_species("https://api.gbif.org/v1/species/match?kingdom=Fungi&name=", species_name)

        # Tester si l'orthographe est bonne sauf pour quelques espèces
        if species_name not in Constants.default_species_writing:
            if species_name != gbif_species.species:
                print("Orthographe douteuse, peut-être plutôt: " + gbif_species.species)
                error_row = pd.DataFrame({'Ligne': [""], 'Espèce': [species_name],
                                          "Type d'erreur": ["Orthographe douteuse, peut-être plutôt: " +
                                                            gbif_species.species]})
                errors = pd.concat([errors, error_row], ignore_index=True, axis=0)

        # Si l'espèce n'est pas l'espèce acceptée, changer l'espèce GBIF
        if gbif_species.status != "ACCEPTED":
            gbif_species = get_gbif_species("https://api.gbif.org/v1/species/", str(gbif_species.accepted_key))
            print("Espèce actuelle selon GBIF: " + gbif_species.species)

        if gbif_species.rank == "SPECIES" or gbif_species.rank == "VARIETY" or gbif_species.rank == "SUBSPECIES" \
                or gbif_species.rank == "FORM":

            # Gestion des espèces dont la synonymie GBIF est incorrecte
            if species_name in Constants.gbif_synonyms_errors:
                gbif_species = Constants.gbif_synonyms_errors.get(species_name)

            species.at[row.Index, "Espèce actuelle"] = gbif_species.species
            species.at[row.Index, "Phylum"] = gbif_species.phylum
            species.at[row.Index, "Ordre"] = gbif_species.order

        else:
            print(species_name + " non récupérée par GBIF")
            error_row = pd.DataFrame({'Ligne': [row.Index + 2], 'Espèce': [species_name],
                                      "Type d'erreur": ["L'espèce n'a pas été trouvée par GBIF"]})
            errors = pd.concat([errors, error_row], ignore_index=True, axis=0)

    return species, errors


def get_gbif_species(url: str, query: str) -> Species:
    try:
        query = urllib.parse.quote(query)
        response = urllib.request.urlopen(url + query)

        json_data = response.read().decode("utf-8", "replace")
        gbif_match = json.loads(json_data)
        return Species(gbif_match["canonicalName"],
                       gbif_match["phylum"] if "phylum" in gbif_match else None,
                       gbif_match["order"] if "order" in gbif_match else None,
                       gbif_match["rank"],
                       gbif_match["taxonomicStatus"] if "taxonomicStatus" in gbif_match else gbif_match["status"],
                       gbif_match["key"] if "key" in gbif_match else gbif_match["usageKey"],
                       gbif_match["acceptedUsageKey"] if "acceptedUsageKey" in gbif_match else None)

    except (urllib.error.URLError, urllib.error.HTTPError) as e:
        print("Problème de connexion à GBIF... Etes-vous connecté à internet ?")
        exit()
