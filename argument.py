from sentence import Sentence


class Argument:
    """Contains the components of an argument, including the premises and the conclusion."""

    def __init__(self, premises: list[Sentence], conclusion: Sentence):
        """Constructor for the Argument class. Initializes the components of the argument.

        :param premises: The premises of the argument.
        :param conclusion: The conclusion of the argument.
        """
        # The premises of the argument, stored as a list.
        self.premises = premises
        # The conclusion sentence of the argument.
        self.conclusion = conclusion

    def get_all_sentences(self) -> list[Sentence]:
        """Returns all sentences in this argument as a list."""
        return self.premises + [self.conclusion]
