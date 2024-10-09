from argument import Argument


def atomic_sentence_truth_value_loop(test_argument: Argument, atomic_sentences_list: list,
                                     atomic_sentence_truth_values: dict[str, bool], index: int) -> bool:
    """One level of the loops that makes all the combinations of atomic sentence truth values. This function uses
    recursion to create loops for all the atomic sentences.

    :param test_argument: The argument we want to test for validity.
    :param atomic_sentences_list: The list of all atomic sentences in the argument to test.
    :param atomic_sentence_truth_values: The current set of atomic sentence truth value combination.
    :param index: The index to seek the atomic sentence for this level of loop from the `atomic_sentences_list`.
    :return: Whether there is evidence of fallacy detected in this level of loop. True for no evidence of fallacy, and
    False for fallacy detected.
    """
    # A list to store the conclusions from the lower level (embedded) loops.
    lower_level_loop_conclusions = list()
    # Loop through False and True for each argument.
    for current_atomic_sentence_truth_value in [False, True]:
        # Store the current truth value for the atomic sentence being treated at this level in the
        # atomic_sentence_truth_values dictionary.
        atomic_sentence_truth_values[atomic_sentences_list[index]] = current_atomic_sentence_truth_value
        # If this is the innermost layer of the embedded loops, we have a complete combination of atomic sentence
        # truth values, and we can test the truth value of the premise and the conclusion.
        if index >= len(atomic_sentences_list) - 1:
            # A variable to keep track of whether all the premises are true in this combination. When the loop below
            # has completed, this variable should reflect whether all the premises are true in this combination.
            premise_all_true = True
            # We loop thorough all premises in this argument to test whether they are true.
            for premise in test_argument.premises:
                # If a premise is not true, we note that down, and break out of this loop to try the next combination
                # of atomic sentence truth values.
                if not premise.get_truth_value(atomic_sentence_truth_values):
                    premise_all_true = False
                    break
                # Otherwise, we continue to test the next premise.
                else:
                    pass
            # If the premises are all true under this combination, but the conclusion is false, then it is proof of
            # invalidity.
            if premise_all_true and not test_argument.conclusion.get_truth_value(atomic_sentence_truth_values):
                # We project the discovery of fallacy to the upper level loops.
                return False
        # If this is not yet the innermost loop to create the truth value combinations, we use recursion to dig down
        # one more level.
        else:
            lower_level_loop_conclusions.append(atomic_sentence_truth_value_loop(test_argument, atomic_sentences_list,
                                                                                 atomic_sentence_truth_values,
                                                                                 index + 1))

    # We project fallacy discoveries to the upper level loops. If the loop at this level received a False,
    # we give the upper level loop the same value to signal that fallacy has been detected.
    return not (False in lower_level_loop_conclusions)


def test_validity(test_argument: Argument) -> bool:
    """Tests the validity of an argument.

    :param test_argument: The argument to be tested for validity.
    :return: Whether this argument is valid.
    """
    # All the atomic sentences included in the argument.
    atomic_sentences = set()
    # Dictionary storing the current combination of atomic sentence truth values.
    atomic_sentences_truth_values = dict()
    # List of all atomic sentences.
    atomic_sentences_list = list()

    # Generate the `atomic_sentences` list.
    all_sentences = test_argument.get_all_sentences()
    for sentence in all_sentences:
        sentence.get_atomic_sentences(atomic_sentences)

    # Generate the `atomic_sentences_truth_values` dictionary. `True` is only used as a placeholder here.
    for atomic_sentence in atomic_sentences:
        atomic_sentences_truth_values.update({atomic_sentence: True})

    # Generate the list of atomic sentences.
    for atomic_sentence in atomic_sentences:
        atomic_sentences_list.append(atomic_sentence)

    # We loop through all combinations of truth values for the atomic sentences, and report the result.
    return atomic_sentence_truth_value_loop(test_argument, atomic_sentences_list, atomic_sentences_truth_values, 0)
