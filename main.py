from logical_connectives import LogicalConnectives
from sentence import Sentence
from argument import Argument
from validity_test import test_validity

premise_1 = Sentence(
    Sentence(
        "A",
        LogicalConnectives.LC_AND,
        "B"),
    LogicalConnectives.LC_CONDITIONAL,
    "C"
)
premise_2 = Sentence("A", LogicalConnectives.LC_OR, "D")
premise_3 = Sentence("", LogicalConnectives.LC_NOT, "D")
premise_4 = Sentence(
    Sentence("",
             LogicalConnectives.LC_NOT,
             Sentence(
                 Sentence("", LogicalConnectives.LC_NOT, "D"),
                 LogicalConnectives.LC_AND,
                 "E")
             ),
    LogicalConnectives.LC_OR,
    "B"
)
premise_5 = Sentence("", LogicalConnectives.LC_NOT, "E")
conclusion = Sentence("", LogicalConnectives.LC_IS, "C")

my_argument = Argument([premise_1, premise_2, premise_3, premise_4, premise_5], conclusion)

valid = test_validity(my_argument)

print("This argument is " + ("valid" if valid else "invalid"))
