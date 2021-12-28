from typing import *

import test_ex11


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
            return self.diagnose_helper(symptoms, current_node.positive_child)
        else:
            return self.diagnose_helper(symptoms, current_node.negative_child)

    def calculate_success_rate(self, records: list[Record]):
        """
        calculate the success rate for all the illness in records
        :param records: List of records
                        record.illness == “covid-19”
                        record.symptoms == [“fever”, “fatigue”, “headache”, “nausea”]
        :return: success rate
        """
        count = 0
        # TODO check if using of value error is correct
        if len(records) == 0:
            raise ValueError('not good, records is empty')
        else:
            for record in records:
                diagnose = self.diagnose(record.symptoms)
                if diagnose == record.illness:
                    count += 1
            return count / len(records)

    def all_illnesses(self):
        """
        the method will use the root of the class in return list of all illnesses
        :return:
        """
        all_illnesses_lst = list()
        return list(set(self.all_illnesses_helper(self.root, all_illnesses_lst)))

    def all_illnesses_helper(self, current_node: Node, all_illnesses_lst: List):
        """

        :return:
        """
        if current_node.negative_child is None:  # check if is leaf
            if current_node.data is None:
                return []
            else:
                return [current_node.data]

        pos = self.all_illnesses_helper(current_node.positive_child, all_illnesses_lst)
        neg = self.all_illnesses_helper(current_node.negative_child, all_illnesses_lst)
        return  neg + pos

    def paths_to_illness(self, illness):
        """
        building path of Bool list to the illness
        :param illness: None str of the ilness that we want to find the path
        :return: list of lists with the path
        """
        current_node = self.root
        current_path = list()
        return self.paths_to_illness_helper(illness, current_node, current_path)

    def paths_to_illness_helper(self, illness, current_node: Node, current_path: List):
        """
        building path of Bool list to the illness
        :param illness: None str of the illness that we want to find the path
        :param current_node:
        :param current_path:
        :param paths:
        :return: list of lists with the path
        """
        if current_node.negative_child is None:
            if current_node.data == illness:
                return [current_path]
            else:
                return list()

        positive = self.paths_to_illness_helper(illness, current_node.positive_child, current_path + [True])
        negtive = self.paths_to_illness_helper(illness, current_node.negative_child, current_path + [False])
        return positive + negtive


def symptoms_valid(symptoms):
    """
    check if all the symptoms are string
    :param symptoms: List of objects
    :return: True if does and False otherwise
    """
    for symptom in symptoms:
        if type(symptom) != str:
            return False
    return True


def records_valid(records):
    """
    check if all the symptoms are string
    :param symptoms: List of objects
    :return: True if does and False otherwise
    """
    for record in records:
        if type(records) != Record:
            return False
    return True


def build_tree(records, symptoms):
    """

    :param records: List of record object
    :param symptoms: List of symptoms
    :return:
    """

    if records_valid(records) and symptoms_valid(symptoms):
        root = Node(symptoms[0])
        build_tree_helper(records, symptoms, root, list(symptoms[0]))
        return Diagnoser(root)
    else:
        raise TypeError()


def chose_from_records(records, filtered_in_symptoms, filtered_out_symptoms):
    """
    choosing the the illnes from the records
    :param records: List of record object
                                    constructor -> Record (illness, symptoms)
                                    record.illness == “covid-19”
                                    record.symptoms == [“fever”, “fatigue”, “headache”, “nausea”]
    :param filtered_in_symptoms:
    :param filtered_out_symptoms:

    :return: illness
    """
    for record in records:
        same_symptoms = set(record.symptoms).intersection(set(filtered_in_symptoms))
        different_symptoms = set(record.symptoms).intersection(set(filtered_out_symptoms))
        if same_symptoms and not different_symptoms:
            return record.illness
        else:
            return None


def build_tree_helper(records, symptoms, current_node, filtered_in_symptoms):
    """

    :param records:
    :param symptoms:
    :param current_node: direction
    :param filtered_in_symptoms:
    :param filtered_out_symptoms:
    :return:
    """
    if not symptoms:  # check if it is leaf
        disease = chose_from_records(records, filtered_in_symptoms, set(symptoms).difference(set(filtered_in_symptoms)))
        return disease
    filtered_in_symptoms.append(symptoms[1])  # TODO some how i need to filltered only the symptoms of good child node
    current_node.positive_child = Node(symptoms[1])
    current_node.negative_child = Node(symptoms[1])

    build_tree_helper(records, symptoms[1:], current_node.positive_child, filtered_in_symptoms)
    build_tree_helper(records, symptoms[1:], current_node.negative_child, filtered_in_symptoms)


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
