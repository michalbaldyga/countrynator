from Leaf import Leaf
from DecisionNode import DecisionNode
from Question import Question
from utils import *


class Tree:
    def __init__(self):
        self.headers = load_headers()

    def build_tree(self, rows):
        gain, question = self.find_best_split(rows)

        if gain == 0:
            return Leaf(rows)
        true_rows, false_rows = self.partition(rows, question)

        true_branch = self.build_tree(true_rows)
        false_branch = self.build_tree(false_rows)

        return DecisionNode(question, true_branch, false_branch)

    def find_best_split(self, rows):
        """Find the best question to ask by iterating over every feature / value
        and calculating the information gain."""
        best_gain = 0
        best_question = None
        current_uncertainty = self.gini(rows)
        n_features = len(rows[0]) - 1

        for col in range(n_features):

            values = set([row[col] for row in rows])
            values = sorted(values)

            for val in values:

                question = Question(col, val, self.headers)
                true_rows, false_rows = self.partition(rows, question)

                if len(true_rows) == 0 or len(false_rows) == 0:
                    continue
                gain = self.info_gain(true_rows, false_rows, current_uncertainty)

                if gain >= best_gain:
                    best_gain, best_question = gain, question

        return best_gain, best_question

    def partition(self, rows, question):
        """Partitions a dataset.

        For each row in the dataset, check if it matches the question. If
        so, add it to 'true rows', otherwise, add it to 'false rows'.
        """
        true_rows, false_rows = [], []
        for row in rows:
            if question.match(row):
                true_rows.append(row)
            else:
                false_rows.append(row)
        return true_rows, false_rows

    def gini(self, rows):
        """Calculate the Gini Impurity for a list of rows."""
        counts = country_names(rows)
        impurity = 1
        for _ in counts:
            prob_of_lbl = 1 / float(len(rows))
            impurity -= prob_of_lbl ** 2
        return impurity

    def info_gain(self, left, right, current_uncertainty):
        """Information Gain.

        The uncertainty of the starting node, minus the weighted impurity of
        two child nodes.
        """
        p = float(len(left)) / (len(left) + len(right))
        return current_uncertainty - p * self.gini(left) - (1 - p) * self.gini(right)