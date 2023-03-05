from utils import country_names


class Leaf:
    # A Leaf node classifies data.

    def __init__(self, rows):
        self.predictions = country_names(rows)
