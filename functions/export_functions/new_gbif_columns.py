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

        try:
            name_url = urllib.parse.quote(species_name)
            response = urllib.request.urlopen(
                "https://api.gbif.org/v1/species/match?kingdom=Fungi&name=" + name_url)

            json_data = response.read().decode("utf-8", "replace")
            gbif_match = json.loads(json_data)
            gbif_species = Species(gbif_match["canonicalName"], gbif_match["phylum"] if "phylum" in gbif_match else "",
                                   gbif_match["order"] if "order" in gbif_match else "", gbif_match["rank"])

            # Tester si l'orthographe est bonne sauf pour quelques espèces
            if species_name not in Constants.default_species_writing:
                if species_name != gbif_species.species:
                    print("Orthographe douteuse, peut-être plutôt: " + gbif_species.species)
                    error_row = pd.DataFrame({'Ligne': [""], 'Espèce': [species_name],
                                              "Type d'erreur": ["Orthographe douteuse, peut-être plutôt: " +
                                                                gbif_species.species]})
                    errors = pd.concat([errors, error_row], ignore_index=True, axis=0)

            # Si l'espèce n'est pas l'espèce acceptée, changer l'espèce GBIF
            if "acceptedUsageKey" in gbif_match:
                accepted_key = gbif_match["acceptedUsageKey"]

                try:
                    response = urllib.request.urlopen(
                        "https://api.gbif.org/v1/species/" + str(accepted_key))

                    json_data = response.read().decode("utf-8", "replace")
                    gbif_match = json.loads(json_data)
                    gbif_species = Species(gbif_match["canonicalName"],
                                           gbif_match["phylum"] if "phylum" in gbif_match else "",
                                           gbif_match["order"] if "order" in gbif_match else "", gbif_match["rank"])
                    print("Espèce actuelle selon GBIF: " + gbif_species.species)

                except urllib.error.HTTPError as e:
                    print("Erreur de communication avec GBIF: erreur " + str(e.code))

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
        except urllib.error.HTTPError as e:
            print("Erreur de communication avec GBIF: erreur " + str(e.code))

    return species, errors
