class Species:
    def __init__(self, species, phylum, order, rank):
        self.species = correction_canonical_name_var(species, rank)
        self.phylum = phylum
        self.order = order
        self.rank = rank


def correction_canonical_name_var(species, rank) -> str:
    # Corriger canonical name pour les variétés, formes et sous-espèces
    if rank == "VARIETY" or rank == "SUBSPECIES" or rank == "FORM":

        split_canonical_name = species.split(" ")
        if rank == "VARIETY":
            term = "var."
        elif rank == "FORM":
            term = "fo."
        else:
            term = "subsp."

        return split_canonical_name[0] + " " + split_canonical_name[1] \
               + " " + term + " " + split_canonical_name[2]

    else:
        return species
