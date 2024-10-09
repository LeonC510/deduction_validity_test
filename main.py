from logical_connectives import LogicalConnectives
from sentence import Sentence
from argument import Argument
from validity_test import test_validity

# This is an example demonstrating the adaptability of this program.
# The following code tests the argument
# (A & B) → C
# A ∨ D
# ¬D
# ¬(¬D & E) ∨ B
# ¬E
# ∴, C
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
premise_5 = Sentence("", LogicalConnectives.LC_IS, "E")
conclusion = Sentence("", LogicalConnectives.LC_IS, "C")

valid = test_validity(Argument([premise_1, premise_2, premise_3, premise_4, premise_5], conclusion))

print("This argument is " + ("valid" if valid else "invalid") + ".")
