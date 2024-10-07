from logical_connectives import LogicalConnectives
from sentence import Sentence
from argument import Argument
from validity_test import test_validity

premise_1 = Sentence("A", LogicalConnectives.LC_OR, "B")
premise_2 = Sentence("", LogicalConnectives.LC_NOT, "B")
premise_3 = Sentence(premise_1, LogicalConnectives.LC_AND, "C")
premise_4 = Sentence(premise_3, LogicalConnectives.LC_AND, premise_1)
conclusion_left = Sentence("A", LogicalConnectives.LC_AND, "B")
conclusion_right = Sentence("", LogicalConnectives.LC_IS, "C")
conclusion = Sentence(conclusion_left, LogicalConnectives.LC_AND, conclusion_right)

my_argument = Argument([premise_1, premise_2, premise_3, premise_4], conclusion)

test_validity(my_argument)
