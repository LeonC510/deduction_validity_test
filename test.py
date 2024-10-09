from sentence import Sentence
from logical_connectives import LogicalConnectives

test = ""
test = Sentence("", LogicalConnectives.LC_IS, "")

print(type(test) == Sentence)