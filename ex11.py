from typing import *
from itertools import combinations

import test_ex11


class Node:
    def __init__(self, data, positive_child=None, negative_child=None):
        self.data = data
        self.positive_child = positive_child
        self.negative_child = negative_child

    def minimize_helper(self, remove_empty=False):
        """
        Replacing the decision tree with an equivalent tree where we lowered unnecessary vertices
        :param self:
        :param remove_empty:
        :return:
        """
        if self.positive_child is None and self.negative_child is None:
            return False
        # if remove_empty is True and current_node.negative_child is None:
        #     current_node = current_node.positive_child
        # if remove_empty is True and current_node.positive_child is None:
        #     current_node = current_node.negative_child
        if self.positive_child.minimize_helper():
            self.positive_child = self.positive_child.positive_child
        if self.negative_child.minimize_helper():
            self.negative_child = self.negative_child.negative_child

        if self.same_roots(self.negative_child, self.positive_child):
            return True

    def same_roots(self, root1, root2):
        if root1 == root2:
            return True
        else:
            return False



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

    def calculate_success_rate(self, records: list[Record]) -> float:
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

    def sorted_by_freq(self, not_sorted) -> List:
        sorted_list = sorted(not_sorted, key=not_sorted.count, reverse=True)
        sorted_no_duplicates = list()
        for string in sorted_list:
            if string not in sorted_no_duplicates:
                sorted_no_duplicates.append(string)
        return sorted_no_duplicates

    def all_illnesses(self):
        """
        the method will use the root of the class in return list of all illnesses
        :return:
        """
        all_illnesses_lst = list()
        all_illnesses_not_sorted = self.all_illnesses_helper(self.root, all_illnesses_lst)
        all_illnesses_sorted = self.sorted_by_freq(all_illnesses_not_sorted)

        return all_illnesses_sorted

    def all_illnesses_helper(self, current_node: Node, all_illnesses_lst: List):
        """

        :return:
        """
        if current_node.negative_child is None:  # check if is leaf
            if current_node.data is None:  # or current_node.data in all_illnesses_lst
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

    def minimize(self, remove_empty=False):
        """
        Replacing the decision tree with an equivalent tree where we lowered unnecessary vertices
        :param self:
        :param remove_empty:
        :return:
        """
        self.minimize_helper()


def symptoms_not_valid(symptoms):
    """
    check if all the symptoms are string
    :param symptoms: List of objects
    :return: True if does and False otherwise
    """
    for symptom in symptoms:
        if type(symptom) != str:
            raise TypeError('bad symptoms')
    return False


def records_not_valid(records):
    """
    check if all the records are Record Type
    :param records: List of objects
    :return: True if does and False otherwise
    """
    for record in records:
        if type(record) != Record:
            raise TypeError('bad records')
    return False


def empty_symptoms(symptoms: List, records: List[Record]) -> bool:
    """
    check if the symptoms are empty or dont match any of the records disease
    or if none of the symptoms are in the records disease
    :param symptoms:
    :param records:
    :return: True if Does and False else
    """
    if not symptoms:
        return True
    # else:
    #     illness_list = all_record_illness(records)
    #     if not set(symptoms).intersection(set(illness_list)):  # check if it empty
    #         return True


def all_record_illness(records):
    """
    find all the records illness
    :param records:
    :return:
    """
    illness_list = list()
    for record in records:
        illness_list.append(record.illness)
    return illness_list


def common_disease(records):
    """

    :param records:
    :return:
    """
    illness_list = all_record_illness(records)
    maximum_impressions = max(illness_list, key=illness_list.count)
    return maximum_impressions


def build_tree(records, symptoms):
    """

    :param records: List of record object
    :param symptoms: List of symptoms
    :return:
    """
    if records_not_valid(records) or symptoms_not_valid(symptoms):
        raise TypeError('input of records or symptoms are not correct')
    # if empty_symptoms(symptoms, records):
    #      maximum_impressions = common_disease(records)
    #      commom_root = Diagnoser(Node(maximum_impressions))
    #      return commom_root
    else:
        root = Node(None)
        filtered_pos_sym = []
        filtered_neg_sym = []
        build_tree_helper(records, symptoms[:], root, filtered_pos_sym, filtered_neg_sym)
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
        flag = True
        for pos_sym in filtered_pos_sym:
            if pos_sym not in record.symptoms:
                flag = False
        for neg_sym in filtered_neg_sym:
            if neg_sym in record.symptoms:
                flag = False
        if flag:
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
        current_node.data = disease
        return
    current_node.data = symptoms[0]
    current_node.positive_child = Node(None)
    current_node.negative_child = Node(None)

    pos = filtered_pos_sym[:]
    pos.append(current_node.data)
    neg = filtered_neg_sym[:]
    build_tree_helper(records, symptoms[1:], current_node.positive_child, pos, neg)
    pos = pos[:-1]
    neg.append(current_node.data)
    build_tree_helper(records, symptoms[1:], current_node.negative_child, pos, neg)


def optimal_tree(records, symptoms, depth):
    if depth == 0:
        return Diagnoser(Node(None))
    if depth < 0 or depth > len(symptoms):
        raise ValueError('Bad depth')
    if len(symptoms) is not len(set(symptoms)):
        raise ValueError('symptoms depth')
    maxi = - depth
    current_root = Node(None)
    for x in combinations(symptoms, depth):
        tree = build_tree(records, x)
        rate = tree.calculate_success_rate(records)
        if maxi < rate:
            maxi = rate
            current_root = tree.root
    return Diagnoser(current_root)


# import pydot
#
#
# def tree_to_graph(tree, graph):
#     if not tree.positive_child:
#         label = 'None' if tree.data is None else tree.data
#         leaf = pydot.Node(id(tree), label=label, shape="box")
#         graph.add_node(leaf)
#         return leaf
#
#     root = pydot.Node(id(tree), label=tree.data, shape="circle")
#     graph.add_node(root)
#     pos_node = tree_to_graph(tree.positive_child, graph)
#     graph.add_edge(pydot.Edge(root, pos_node, label="Yes"))
#
#     neg_node = tree_to_graph(tree.negative_child, graph)
#     graph.add_edge(pydot.Edge(root, neg_node, label="No"))
#
#     return root
#
#
# def draw_tree(tree, filename):
#     graph = pydot.Dot(graph_type='graph')
#     tree_to_graph(tree, graph)
#     graph.write(filename)


if __name__ == "__main__":
    pass
    # record1 = Record("influenza", ["cough", "fever"])
    # record2 = Record("cold", ["cough"])
    # record3 = Record("covid-19", ["headache"])
    # records = [record1, record2]
    # x = build_tree(records, ["fever"])
    # draw_tree(x.root, "Tree.txt")

    # symptoms = ['a', 'b', 'd', 'g', 'k', 'a']
    # records = parse_data("test_all_illnesses.txt")
    # tree = build_tree(records, symptoms)
    # draw_tree(tree.root, "Tree.txt")
