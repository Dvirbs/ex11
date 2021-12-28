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
        return self.all_illnesses_helper(self.root, all_illnesses_lst)

    def all_illnesses_helper(self, current_node: Node, all_illnesses_lst: List):
        """

        :return:
        """
        if current_node.negative_child is None:  # check if is leaf
            if current_node.data is None or current_node.data in all_illnesses_lst:
                return []
            else:
                all_illnesses_lst.append(current_node.data)
                return [current_node.data]

        pos = self.all_illnesses_helper(current_node.positive_child, all_illnesses_lst)
        neg = self.all_illnesses_helper(current_node.negative_child, all_illnesses_lst)
        return neg + pos

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


def symptoms_not_valid(symptoms):
    """
    check if all the symptoms are string
    :param symptoms: List of objects
    :return: True if does and False otherwise
    """
    for symptom in symptoms:
        if type(symptom) != str:
            return True
    return False


def records_not_valid(records):
    """
    check if all the records are Record Type
    :param records: List of objects
    :return: True if does and False otherwise
    """
    for record in records:
        if type(record) != Record:
            return True
    return False


def build_tree(records, symptoms):
    """

    :param records: List of record object
    :param symptoms: List of symptoms
    :return:
    """
    if records_not_valid(records) or symptoms_not_valid(symptoms):
        raise TypeError('input of records or symptoms are not correct')
    else:
        root = Node(symptoms[0])
        filtered_pos_sym = []
        filtered_neg_sym = []
        build_tree_helper(records, symptoms[1:], root, filtered_pos_sym, filtered_neg_sym)
        return Diagnoser(root)


def chose_from_records(records, filtered_pos_sym, filtered_neg_sym) -> Optional[str]:
    """
    choosing the the illnes from the records
    :param records: List of record object
    :param filtered_in_symptoms:
    :param filtered_out_symptoms:

    :return: Node that is illness
    """
    illness_list = list()
    for record in records:
        positive_path_symptoms = set(record.symptoms).intersection(set(filtered_pos_sym))
        not_in_negative_path_symptoms = set(record.symptoms).difference(set(filtered_neg_sym))
        if not_in_negative_path_symptoms and positive_path_symptoms:
            illness_list.append(record.illness)
    if illness_list:
        maximum_impressions = max(illness_list, key=illness_list.count)
        return maximum_impressions
    else:
        return None


def build_tree_helper(records, symptoms, current_node, filtered_pos_sym, filtered_neg_sym):
    """

    :param records:
    :param symptoms:
    :param current_node: direction
    :param filtered_in_symptoms:
    :param filtered_out_symptoms:
    :return:
    """
    if not symptoms:  # check if it is leaf
        disease: Optional[str] = chose_from_records(records, filtered_pos_sym, filtered_neg_sym)
        current_node = Node(disease)
        return current_node
    current_node.positive_child = Node(symptoms[0])
    current_node.negative_child = Node(symptoms[0])

    pos = filtered_pos_sym[:]
    pos.append(symptoms[0])
    neg = filtered_neg_sym[:]
    current_node.positive_child = build_tree_helper(records, symptoms[1:], current_node.positive_child, pos, neg)
    pos = pos[:-1]
    neg.append(symptoms[0])
    current_node.negative_child = build_tree_helper(records, symptoms[1:], current_node.negative_child, pos, neg)


def optimal_tree(records, symptoms, depth):
    if depth == 0:
        return Diagnoser(Node(None))
    elif depth < 0 or depth > len(symptoms):
        raise ValueError


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
