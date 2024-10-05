from logical_connectives import LogicalConnectives
from sentence import Sentence
from argument import Argument
from validity_test import validity_tester

premise_1 = Sentence("A", LogicalConnectives.LC_OR, "B")
premise_2 = Sentence("", LogicalConnectives.LC_NOT, "B")
premise_3 = Sentence(premise_1, LogicalConnectives.LC_AND, "C")
premise_4 = Sentence(premise_3, LogicalConnectives.LC_AND, premise_1)
conclusion = Sentence("", LogicalConnectives.LC_IS, "A")

my_argument = Argument([premise_1, premise_2, premise_3, premise_4], conclusion)

my_validity_tester = validity_tester(my_argument)
