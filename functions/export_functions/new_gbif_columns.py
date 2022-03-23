import urllib.request
import json

import pandas as pd


def new_gbif_columns(species: pd.DataFrame):
    errors = pd.DataFrame([], )
    species["Espèce actuelle"] = None
    species["Phylum"] = None
    species["Ordre"] = None
    for row in species.itertuples():

        species_name = row.Espèce

        try:
            name_url = urllib.parse.quote(row.Espèce)
            response = urllib.request.urlopen(
                "https://api.gbif.org/v1/species/match?kingdom=Fungi&name=" + name_url)

            json_data = response.read().decode("utf-8", "replace")
            gbif_match = json.loads(json_data)

            canonical_name = gbif_match["canonicalName"]
            rank = gbif_match["rank"]

            if rank == "SPECIES" or rank == "VARIETY" or rank == "SUBSPECIES" or rank == "FORM":

                # Corriger canonical name pour les variétés, formes et sous-espèces
                if rank == "VARIETY" or rank == "SUBSPECIES" or rank == "FORM":

                    split_canonical_name = canonical_name.split(" ")
                    if rank == "VARIETY":
                        term = "var."
                    elif rank == "FORM":
                        term = "fo."
                    else:
                        term = "subsp."

                    canonical_name = split_canonical_name[0] + " " + split_canonical_name[1] + " " + term \
                                     + " " + split_canonical_name[2]

                # Gestion des espèces dont la synonymie GBIF est incorrecte
                if species_name == "Tubaria hiemalis":
                    species.at[row.Index, "Espèce actuelle"] = "Tubaria hiemalis"
                    species.at[row.Index, "Phylum"] = "Basidiomycota"
                    species.at[row.Index, "Ordre"] = "Agaricales"
                elif species_name == "Galerina autumnalis":
                    species.at[row.Index, "Espèce actuelle"] = "Galerina autumnalis"
                    species.at[row.Index, "Phylum"] = "Basidiomycota"
                    species.at[row.Index, "Ordre"] = "Agaricales"
                else:
                    species.at[row.Index, "Espèce actuelle"] = canonical_name

                    # Tester si l'orthographe est bonne
                    if species_name != canonical_name:
                        print("Erreur d'orthographe ? : " + species_name)
                        error_row = pd.DataFrame({'Ligne': [""], 'Espèce': [species_name],
                                                  "Type d'erreur": ["Peut-être plutôt: " +
                                                                    canonical_name]})
                        errors = pd.concat([errors, error_row], ignore_index=True, axis=0)

                    if "phylum" in gbif_match:
                        species.at[row.Index, "Phylum"] = gbif_match["phylum"]

                    if "order" in gbif_match:
                        species.at[row.Index, "Ordre"] = gbif_match["order"]

                    if "acceptedUsageKey" in gbif_match:
                        accepted_key = gbif_match["acceptedUsageKey"]

                        try:
                            response = urllib.request.urlopen(
                                "https://api.gbif.org/v1/species/" + str(accepted_key))

                            json_data = response.read().decode("utf-8", "replace")
                            gbif_species = json.loads(json_data)

                            species.at[row.Index, "Espèce actuelle"] = gbif_species["canonicalName"]
                            if "phylum" in gbif_match:
                                species.at[row.Index, "Phylum"] = gbif_species["phylum"]

                            if "order" in gbif_match:
                                species.at[row.Index, "Ordre"] = gbif_species["order"]

                            print("Espèce actuelle: " + gbif_species["canonicalName"])

                        except:
                            print("Erreur de communication avec GBIF")

            else:
                print(species_name + " non récupérée par GBIF")
                error_row = pd.DataFrame({'Ligne': [row.Index + 2], 'Espèce': [species_name],
                                          "Type d'erreur": ["L'espèce n'a pas été trouvée par GBIF"]})
                errors = pd.concat([errors, error_row], ignore_index=True, axis=0)
        except:
            print("Erreur de communication avec GBIF")
        finally:
            print(species_name)

    return species, errors
