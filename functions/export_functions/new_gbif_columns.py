import urllib.request
import json

import pandas as pd


def new_gbif_columns(species: pd.DataFrame):
    errors = pd.DataFrame
    species["Espèce actuelle"] = None
    species["Phylum"] = None
    species["Ordre"] = None
    for row in species.itertuples():
        try:
            name_url = urllib.parse.quote(row.Espèce)
            response = urllib.request.urlopen(
                "https://api.gbif.org/v1/species/match?kingdom=Fungi&name=" + name_url)

            json_data = response.read().decode("utf-8", "replace")
            gbif_match = json.loads(json_data)
            if gbif_match["rank"] == "SPECIES" or gbif_match["rank"] == "VARIETY" \
                    or gbif_match["rank"] == "SUBSPECIES" or gbif_match["rank"] == "FORM":

                species.at[row.Index, "Espèce actuelle"] = gbif_match["canonicalName"]
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
                print(row.Espèce + " non récupérée par GBIF")
                error_row = pd.DataFrame({'Ligne': [row.Index + 2], 'Espèce': [row.Espèce],
                                          "Type d'erreur": ["L'espèce n'a pas été trouvée par GBIF"]})
                errors = pd.concat([errors, error_row], ignore_index=True, axis=0)
        except:
            print("Erreur de communication avec GBIF")
        finally:
            print(row.Espèce)

    return species, errors
