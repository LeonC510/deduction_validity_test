from logical_connectives import connective_truth_tables
from logical_connectives import LogicalConnectives


class Sentence:
    """Stores the properties and methods related to a Sentence."""
    def get_truth_value(self, atomic_sentence_truth_values: dict[str, bool]) -> bool:
        """Get the truth value of this sentence, determined by the truth values of atomic sentences.

        :param atomic_sentence_truth_values: The truth value of atomic sentences.
        :return: The truth value of this sentence, given the truth value of atomic sentences.
        """
        # The list to store the sub sentence truth values in.
        sub_sentence_truth_values = list()
        # Get the truth value of sub sentences.
        for sub_sentence in self.sub_sentences:
            # If the type of the sub sentence is string, then it is an atomic sentence. We seek the truth value from
            # the dictionary passed as parameter.
            if type(sub_sentence) == str:
                # If the sub sentence is an empty string, it is only a placeholder. We can safely ignore it.
                if sub_sentence == "":
                    sub_sentence_truth_values.append(False)
                else:
                    sub_sentence_truth_values.append(atomic_sentence_truth_values[sub_sentence])
            # If it's a `Sentence` object, then we use function recursion to get the truth value of the sub sentence.
            elif type(sub_sentence) == Sentence:
                sub_sentence_truth_values.append(sub_sentence.get_truth_value(atomic_sentence_truth_values))
            # If it's not either of the types, something is wrong.
            else:
                # We raise an exception to let the user know that something is wrong.
                raise Exception("Incorrect sentence type: " + str(type(sub_sentence)))
        # We return the truth value of the whole sentence by searching the truth table corresponding to this
        # sentence's connective.
        return connective_truth_tables[self.connective][tuple(sub_sentence_truth_values)]

    def get_atomic_sentences(self, atomic_sentences: set):
        """Add to the set all the atomic sentences included in this sentence.

        :param atomic_sentences: The set of atomic sentences to add to.
        :return: None.
        """
        # Loop thorough the sub sentences of this sentence.
        for sub_sentence in self.sub_sentences:
            # If the type of `sub_sentence` is a non-empty string, it is an atomic sentence.
            if type(sub_sentence) == str:
                # Unless it is an empty placeholder, we add the sub sentence to the set for use by the caller of this
                # function.
                if sub_sentence != "":
                    atomic_sentences.add(sub_sentence)
                # If it is a placeholder, we can safely ignore it.
                else:
                    continue
            # If the type of `sentence` is `Sentence`, it is not an atomic sentence, and we use recursion to drill
            # one level deeper.
            elif type(sub_sentence) == Sentence:
                sub_sentence.get_atomic_sentences(atomic_sentences)
            # If it's not either of the types, something is wrong. We raise an exception to let the user know.
            else:
                raise Exception("Incorrect sentence type: " + str(type(sub_sentence)))

    def __init__(self, left_sentence, connective: LogicalConnectives, right_sentence):
        """Stores the sentence's sub sentences and connective.

        :param left_sentence: The sub sentence on the left side of the connective. Could be a string (for atomic
        sentences) or list (for compound sentences).
        :param connective: The main logical connective of the sentence.
        :param right_sentence: The sub sentence on the right side of the connective.
        """
        # List for sub sentences.
        self.sub_sentences = [left_sentence, right_sentence]
        # The connective of the sentence.
        self.connective = connective
