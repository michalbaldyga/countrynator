from utils import is_numeric


class Question:
    # A Question is used to partition a dataset.

    def __init__(self, column, value, headers):
        self.column = column
        self.value = value
        self.headers = headers

    def match(self, example):
        val = example[self.column]
        if is_numeric(val):
            return val >= self.value
        else:
            return val == self.value

    def __repr__(self):
        return "Czy " + self.headers[self.column] + "?"
