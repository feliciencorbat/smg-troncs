class Species:
    def __init__(self, species: str, phylum: str, order: str, rank: str):
        self._species = species
        self.phylum = phylum
        self.order = order
        self.rank = rank

    @property
    def species(self):
        # Corriger canonical name pour les variétés, formes et sous-espèces
        if self.rank == "VARIETY" or self.rank == "SUBSPECIES" or self.rank == "FORM":

            split_canonical_name = self._species.split(" ")
            if self.rank == "VARIETY":
                term = "var."
            elif self.rank == "FORM":
                term = "fo."
            else:
                term = "subsp."

            return split_canonical_name[0] + " " + split_canonical_name[1] + " " + term + " " + split_canonical_name[2]
        else:
            return self._species
