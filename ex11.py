from typing import *

class Node:
    def __init__(self, data, positive_child=None, negative_child=None):
        self.data = data
        self.positive_child = positive_child
        self.negative_child = negative_child


class Record:
    def __init__(self, illness, symptoms):
        self.illness = illness
        self.symptoms = symptoms


def parse_data(filepath):
    with open(filepath) as data_file:
        records = []
        for line in data_file:
            words = line.strip().split()
            records.append(Record(words[0], words[1:]))
        return records


class Diagnoser:
    def __init__(self, root: Node):
        self.root = root

    def diagnose(self, symptoms):
        """
        function that find the diagnose from list of symptoms
        :param symptoms: List of symptoms
        :return: the diagnose
        """
        diagnose = self.diagnose_helper(symptoms, self.root)
        return diagnose

    def diagnose_helper(self, symptoms, current_node: Node):
        """
        function that find the diagnose from list of symptoms
        :param symptoms: List of symptoms
        :param current_node: the current node
        :return: the diagnose
        """
        if current_node.negative_child is None:  # check if is leaf
            return current_node.data
        if current_node.data in symptoms:
            self.diagnose_helper(symptoms, current_node.positive_child)
        else:
            self.diagnose_helper(symptoms, current_node.negative_child)

    def calculate_success_rate(self, records: list[Record]):
        """
        calculate the success rate for all the illness in records
        :param records: List of records
        :return: success rate
        """
        count = 0
        try:
            for record in records:
                diagnose = self.diagnose(record.symptoms)
                if diagnose == record.illness:
                    count += 1
            return count/int(len(records))
        except ValueError():
            return "\n*** records is empty! please try again ***"

    def all_illnesses(self, current_node):
        """

        :return:
        """
        # Manually build a simple tree.
        #                cough
        #          Yes /       \ No
        #        fever           healthy
        #   Yes /     \ No
        # covid-19   cold

        all_illnesses_lst = list()
        if current_node.negative_child is None:  # check if is leaf
            all_illnesses_lst.append(current_node.data)
        self.all_illnesses(current_node.positive_child)
        self.all_illnesses(current_node.nagtive_child)

    def paths_to_illness(self, illness):
        pass


def build_tree(records, symptoms):
    pass


def optimal_tree(records, symptoms, depth):
    pass


if __name__ == "__main__":

    # Manually build a simple tree.
    #                cough
    #          Yes /       \ No
    #        fever           healthy
    #   Yes /     \ No
    # covid-19   cold

    flu_leaf = Node("covid-19", None, None)
    cold_leaf = Node("cold", None, None)
    inner_vertex = Node("fever", flu_leaf, cold_leaf)
    healthy_leaf = Node("healthy", None, None)
    root = Node("cough", inner_vertex, healthy_leaf)

    diagnoser = Diagnoser(root)

    # Simple test
    diagnosis = diagnoser.diagnose(["cough"])
    if diagnosis == "cold":
        print("Test passed")
    else:
        print("Test failed. Should have printed cold, printed: ", diagnosis)

# Add more tests for sections 2-7 here.
