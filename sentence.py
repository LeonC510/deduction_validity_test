from logical_connectives import reverse_truth_table


class Sentence:
    def test_value_possible(self, truth_value: bool, sentence_reqs: dict[str, bool] = None) -> (bool, dict[str, bool]):
        """Test whether a given truth value is possible

        :param truth_value: The truth value requirement to test.
        :param sentence_reqs: The atomic sentence truth requirements.
        :return: If the truth value can be fulfilled while the atomic sentence truth requirements are simultaneously
        fulfilled.
        """
        if sentence_reqs is None:
            sentence_reqs = dict()
        test_result = False

        if not self.first_test_value_possible:
            if self.last_truth_value_req != truth_value or self.last_sentence_req != sentence_reqs:
                self.truth_value_combo_iterator = 0

        self.first_test_value_possible = False
        self.last_truth_value_req = truth_value
        self.last_sentence_req = sentence_reqs

        additional_sentence_reqs = dict()
        if self.truth_value_combo_iterator >= len(reverse_truth_table[self.connective][truth_value]):
            return False, additional_sentence_reqs

        for truth_value_combo in reverse_truth_table[self.connective][truth_value][self.truth_value_combo_iterator:]:
            self.truth_value_combo_iterator += 1
            additional_sentence_reqs.clear()
            for sentence_index, sub_sentence in enumerate(self.sub_sentences):
                # If the type of `sentence` is a non-empty string, it is an atomic sentence.
                if type(sub_sentence) == str:
                    # If `sub_sentence` is empty, it is only a placeholder, and we can ignore this sub-sentence
                    if sub_sentence == "":
                        test_result = True
                        continue

                    # If there is no requirements for this atomic sentence, we note the current truth value combo as a
                    # new requirement to be returned to the upper-level function. We then continue to check this combo
                    # for the next sub-sentence.
                    if sentence_reqs.get(sub_sentence) == None:
                        additional_sentence_reqs.update({sub_sentence: truth_value_combo[sentence_index]})
                        test_result = True
                        continue
                    # If there is a requirement for this atomic sentence, but it's the same as the truth value combo
                    # specifies, we keep this combo and test it on the next sub-sentence.
                    elif (truth_value_combo[sentence_index] == {**sentence_reqs, **additional_sentence_reqs}
                            .get(sub_sentence)):
                        test_result = True
                        continue
                    # If there is a requirement for this atomic sentence, but it doesn't fit, then this truth value
                    # combo doesn't work, and we'll try the next truth value combo.
                    else:
                        test_result = False
                        break
                # If the type of `sentence` is `Sentence`, it is not an atomic sentence, and we use recursion to drill
                # one level deeper.
                elif type(sub_sentence) == Sentence:
                    (test_result, temp_additional_sentence_reqs) = sub_sentence.test_value_possible(
                        truth_value_combo[sentence_index],
                        {**sentence_reqs, **additional_sentence_reqs})
                    additional_sentence_reqs.update(temp_additional_sentence_reqs)
                # If it's not either of the types, something is wrong
                else:
                    raise Exception("Incorrect sentence type: " + str(type(sub_sentence)))
            # When we have checked all sub-sentences for this truth value combo and found that this combo works, we
            # break out of the truth value combo loop and return the result.
            if test_result == True:
                break

        return test_result, additional_sentence_reqs

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

