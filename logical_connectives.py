from enum import Enum


class LogicalConnectives(Enum):
    LC_IS = 1           # No connective
    LC_NOT = 2          # "Not" (¬) logical connective
    LC_AND = 3          # "And" (&) logical connective
    LC_OR = 4           # "Or" (∨) logical connective
    LC_CONDITIONAL = 5  # "Conditional" (→) logical connective


# Reverse truth table map from logical connective name to the
# reverse truth table for that connective
reverse_truth_table = {
    # Reverse truth table for the is connective. The left side "True" value isn't really used; it is only a
    # placeholder.
    LogicalConnectives.LC_IS: {
        True: [[True, True]],
        False: [[True, False]]
    },
    # Reverse truth table for the not connective. The left side "True" value isn't really used; it is only a
    # placeholder.
    LogicalConnectives.LC_NOT: {
        True: [[True, False]],
        False: [[True, True]]
    },
    LogicalConnectives.LC_AND: {
        True: [[True, True]],
        False: [[True, False], [False, True], [False, False]]},
    LogicalConnectives.LC_OR: {
        True: [[True, True], [True, False], [False, True]],
        False: [[False, False]]
    },
    LogicalConnectives.LC_CONDITIONAL: {
        True: [[True, True], [False, True], [False, False]],
        False: [[True, False]]
    },
}
