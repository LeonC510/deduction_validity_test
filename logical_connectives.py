from enum import Enum


class LogicalConnectives(Enum):
    """Enums for the kinds of logical connectives this program supports. More can be added in the future."""
    LC_IS = 1           # No connective
    LC_NOT = 2          # "Not" (¬) logical connective
    LC_AND = 3          # "And" (&) logical connective
    LC_OR = 4           # "Or" (∨) logical connective
    LC_CONDITIONAL = 5  # "Conditional" (→) logical connective


# Truth table map to map the logical connective to its respective truth table. The truth tables in this dictionary
# maps a combination of truth values of sub sentences to the truth value of the whole sentence.
connective_truth_tables = {
    # Truth table for the `is` connective. The left side values are not really used; they are only placeholders.
    LogicalConnectives.LC_IS: {
        (True, True): True,
        (True, False): False,
        (False, True): True,
        (False, False): False,
    },
    # Truth table for the `not` connective. The left side values are not really used; they are only placeholders.
    LogicalConnectives.LC_NOT: {
        (True, True): False,
        (True, False): True,
        (False, True): False,
        (False, False): True,
    },
    # Truth table for the `and` connective.
    LogicalConnectives.LC_AND: {
        (True, True): True,
        (True, False): False,
        (False, True): False,
        (False, False): False,
    },
    # Truth table for the `or` connective.
    LogicalConnectives.LC_OR: {
        (True, True): True,
        (True, False): True,
        (False, True): True,
        (False, False): False,
    },
    # Truth table for the `conditional` connective.
    LogicalConnectives.LC_CONDITIONAL: {
        (True, True): True,
        (True, False): False,
        (False, True): True,
        (False, False): True,
    },
}
