from logical_connectives import reverse_truth_table


class Sentence:
    def test_value_possible(self, truth_value: bool, clear_combo_iterator: bool, skip: bool,
                            sentence_reqs: dict[str, bool] = None) \
            -> (bool, dict[str, bool]):
        """Test whether a given truth value is possible

        :param truth_value: The truth value requirement to test.
        :param clear_combo_iterator: Whether to reset the truth value combo iterator.
        :param skip: If True, then this function will not do anything, and just return the values returned last time.
        This should not be set to true when calling this function for the first time.
        :param sentence_reqs: The atomic sentence truth requirements.
        :return: If the truth value can be fulfilled while the atomic sentence truth requirements are simultaneously
        fulfilled.
        """

        if skip:
            if self.last_test_result is None or self.last_additional_truth_value_req is None:
                raise Exception("Not allowed: Calling test_value_possible for the first time with skip set.")
            return self.last_test_result, self.last_additional_truth_value_req

        if sentence_reqs is None:
            sentence_reqs = dict()
        # Whether it's possible to set the sentence's truth value to the one required. Used to return the test result.
        value_possible = False

        if clear_combo_iterator:
            self.truth_value_combo_iterator = 0

        self.first_test_value_possible = False
        self.last_truth_value_req = truth_value
        self.last_sentence_req = sentence_reqs

        additional_sentence_reqs = dict()
        if self.truth_value_combo_iterator >= len(reverse_truth_table[self.connective][truth_value]):
            value_possible = False
            self.last_additional_truth_value_req = additional_sentence_reqs
            self.last_test_result = value_possible
            return value_possible, additional_sentence_reqs

        for truth_value_combo in reverse_truth_table[self.connective][truth_value][self.truth_value_combo_iterator:]:
            more_combo_exist_for_sub_sentences = True
            while more_combo_exist_for_sub_sentences:
                additional_sentence_reqs.clear()
                for sentence_index, sub_sentence in enumerate(self.sub_sentences):
                    # If the type of `sentence` is a non-empty string, it is an atomic sentence.
                    if type(sub_sentence) == str:
                        # If `sub_sentence` is empty, it is only a placeholder, and we can ignore this sub-sentence
                        if sub_sentence == "":
                            value_possible = True
                            continue

                        # If there is no requirements for this atomic sentence, we note the current truth value combo
                        # as a new requirement to be returned to the upper-level function. We then continue to check
                        # this combo for the next sub-sentence.
                        if sentence_reqs.get(sub_sentence) == None:
                            additional_sentence_reqs.update({sub_sentence: truth_value_combo[sentence_index]})
                            value_possible = True
                        # If there is a requirement for this atomic sentence, but it's the same as the truth value combo
                        # specifies, we keep this combo and test it on the next sub-sentence.
                        elif (truth_value_combo[sentence_index] == {**sentence_reqs, **additional_sentence_reqs}
                                .get(sub_sentence)):
                            value_possible = True
                        # If there is a requirement for this atomic sentence, but it doesn't fit, then this truth value
                        # combo doesn't work, and we'll try the next truth value combo.
                        else:
                            value_possible = False
                    # If the type of `sentence` is `Sentence`, it is not an atomic sentence, and we use recursion to drill
                    # one level deeper.
                    elif type(sub_sentence) == Sentence:
                        # We pass the truth value requirements from the reverse truth table to be tested by the sub
                        # sentence, requiring the aggregate atomic sentence truth value requirements up until now. Here,
                        # the `clear_combo_iterator` is always set to True; every time this line runs, we're trying a new
                        # sub sentence truth value combo that makes the sentence fulfill the truth value requirements.
                        # TODO: Index of truth value combo isn't incremented when we attempt to try the next valid truth
                        #  value combo when already found a valid one.
                        (value_possible, temp_additional_sentence_reqs) = sub_sentence.test_value_possible(
                            truth_value_combo[sentence_index], sentence_index >= self.last_impossible_sub_sentence,
                            sentence_index < self.last_impossible_sub_sentence - 1
                            and self.last_impossible_sub_sentence != len(self.sub_sentences),
                            {**sentence_reqs, **additional_sentence_reqs})
                        # We do this if check to avoid adding unnecessary atomic sentence truth value requirements.
                        if value_possible:
                            additional_sentence_reqs.update(temp_additional_sentence_reqs)
                    # If it's not either of the types, something is wrong
                    else:
                        raise Exception("Incorrect sentence type: " + str(type(sub_sentence)))

                    # If it is not possible to meet the truth value combination for this sub sentence, we break out
                    # to test from the beginning.
                    if not value_possible:
                        # If this sentence is the first sub sentence and failed to meet the truth value combination,
                        # then this truth value combination does not work, and we'll test the next one.
                        if sentence_index == 0:
                            more_combo_exist_for_sub_sentences = False
                        self.last_impossible_sub_sentence = sentence_index
                        break

                # When we have checked all sub-sentences for this truth value combo and found that this combo works, we
                # break out of the truth value combo loop and return the result.
                if value_possible:
                    self.last_test_result = value_possible
                    self.last_additional_truth_value_req = additional_sentence_reqs
                    return value_possible, additional_sentence_reqs

            # The index of the sentence that last reported that it's not possible to achieve the requirements. We use
            # the total number of sub sentences as an idle value for when the loop runs for the first time.
            self.last_impossible_sub_sentence = len(self.sub_sentences)
            # Note down that we're trying the next truth value combo so that we can resume the
            # progress next time this function is called.
            self.truth_value_combo_iterator += 1


        self.last_test_result = value_possible
        self.last_additional_truth_value_req = additional_sentence_reqs
        return value_possible, additional_sentence_reqs

    # Find all atomic sentences in the sentence stack included in this sentence
    def get_atomic_sentences(self, atomic_sentences: set):
        for sub_sentence in self.sub_sentences:
            # If the type of `sentence` is a non-empty string, it is an atomic sentence.
            if type(sub_sentence) == str:
                if sub_sentence != "":
                    atomic_sentences.add(sub_sentence)
                else:
                    continue
            # If the type of `sentence` is `Sentence`, it is not an atomic sentence, and we use recursion to drill
            # one level deeper.
            elif type(sub_sentence) == Sentence:
                sub_sentence.get_atomic_sentences(atomic_sentences)
            # If it's not either of the types, something is wrong
            else:
                raise Exception("Incorrect sentence type: " + str(type(sub_sentence)))

    def __init__(self, left_sentence, connective, right_sentence):
        self.sub_sentences = [left_sentence, right_sentence]
        self.connective = connective
        self.first_test_value_possible = True
        self.last_truth_value_req = False
        self.last_sentence_req = {"": False}
        self.truth_value_combo_iterator = 0
        self.last_additional_truth_value_req = None
        self.last_test_result = None
        self.last_impossible_sub_sentence = len(self.sub_sentences)
