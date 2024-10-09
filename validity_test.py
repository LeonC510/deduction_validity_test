import argument


def test_validity(test_argument: argument) -> bool:
    atomic_sentences = set()
    atomic_sentences_truth_values = dict()
    all_sentences = test_argument.get_all_sentences()
    for sentence in all_sentences:
        sentence.get_atomic_sentences(atomic_sentences)

    # Convert the `atomic_sentences` set into a dictionary
    for atomic_sentence in atomic_sentences:
        atomic_sentences_truth_values.update({atomic_sentence: True})

    # Standing requirements for atomic sentences
    conclusion_sentence_reqs = dict()
    # We put this in a loop so that we can test every combination that make the conclusion sentence false.
    while True:
        # We find truth value combos that can make the conclusion sentence False. We always set
        # `clear_combo_iterator` to False here, as there is no situation where we need to iterate over the possible
        # truth value combinations for the conclusion sentence from the start again.
        (conclusion_possible, conclusion_sentence_reqs) = test_argument.conclusion.test_value_possible(False, False,
                                                                                                       False)
        # If all truth value combinations have been tried without any of them allowing all the premises to be true when
        # the conclusion is false, then this argument is valid.
        if not conclusion_possible:
            return True

        # Whether there are more truth value combos that we need to test.
        more_combos_exist_for_premises = True
        # The atomic sentence truth value requirements generated when testing the premises.
        premises_sentence_reqs = dict()
        # The index of the sentence that last reported that it's not possible to achieve the requirements. We use
        # the total number of sub sentences as an idle value for when the loop runs for the first time.
        last_impossible_premise = len(test_argument.premises)
        while more_combos_exist_for_premises:
            for sentence_index, sentence in enumerate(test_argument.premises):
                (premise_possible, current_sentence_reqs) \
                    = sentence.test_value_possible(True,
                                                   sentence_index >= last_impossible_premise,
                                                   sentence_index < last_impossible_premise - 1
                                                   and last_impossible_premise != len(test_argument.premises),
                                                   {**conclusion_sentence_reqs, **premises_sentence_reqs})
                # `premise_possible` being false means that it is not possible for this premise sentence to be true
                # under the requirements set to make the conclusion false and/or to make a premise sentence true,
                # so there is no point in testing the following premises anymore. We break out to the outer loop.
                if not premise_possible:
                    # If it is not possible for this premise to be true, and it is the first premise, it means that
                    # the premises cannot be true at the same time under the requirements set to make the conclusion
                    # false. In this case, we break out to update `conclusion_sentence_reqs` to try the next truth
                    # value combo that would make the conclusion false.
                    if sentence_index == 0:
                        more_combos_exist_for_premises = False
                    # Otherwise, we try the next truth value combo to make the premises true.
                    else:
                        pass    # We don't really need this else block; we only added it to make the comments clearer.
                    # Clear the atomic sentence truth value requirements produced by the premises.
                    premises_sentence_reqs.clear()
                    last_impossible_premise = sentence_index
                    break   # Break out to test the next truth value combo for the premises.
                # Otherwise, we decide whether this is the last premise that we need to test.
                else:
                    # If this premise is the last premise we need to test, and all premises can be simultaneously true
                    # while the conclusion is false, the argument is invalid.
                    if sentence_index == len(test_argument.premises) - 1:
                        return False
                    # Otherwise, we continue to test the next premise.
                    # We add the sentence requirements produced by this premise to the all the requirements.
                    premises_sentence_reqs.update(current_sentence_reqs)
