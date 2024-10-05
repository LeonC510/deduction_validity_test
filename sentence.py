from logical_connectives import reverse_truth_table


class Sentence:
    # TODO: Iterate to the next truth value combo each time this function is called, or iterate all combos each time
    #  this function is called?
    first_test_value_possible = True
    last_truth_value_req = False
    truth_value_combo_iterator = 0
    def test_value_possible(self, truth_value: bool, sentence_reqs: dict[str, bool]) -> (bool, dict[str, bool]):
        """Test whether a given truth value is possible

        :param truth_value: The truth value requirement to test.
        :param sentence_reqs: The atomic sentence truth requirements.
        :return: If the truth value can be fulfilled while the atomic sentence truth requirements are simultaneously
        fulfilled.
        """
        first_test_value_possible = False

        if not first_test_value_possible:
            if truth_value != self.last_truth_value_req:
                self.truth_value_combo_iterator = 0
            else:
                self.truth_value_combo_iterator += 1

        additional_sentence_reqs = dict()
        truth_value_combo = reverse_truth_table[self.connective][truth_value][self.truth_value_iterator]
        for sentence_index, sub_sentence in enumerate(self.sub_sentences):
            # If the type of `sentence` is a non-empty string, it is an atomic sentence.
            if type(sub_sentence) == str:
                # If `sub_sentence` is empty, it is only a placeholder, and we can ignore this sub-sentence
                if sub_sentence == "":
                    continue

                # If there is no requirements for this atomic sentence, we note the current truth value combo as a
                # new requirement to be returned to the upper-level function.
                if sentence_reqs.get(sub_sentence) == None:
                    additional_sentence_reqs.update({sub_sentence: truth_value_combo[sentence_index]})
                    continue
                # If there is a requirement for this atomic sentence, but it's the same as the truth value combo
                # specifies, we keep this combo and test it on the next sub-sentence.
                elif truth_value_combo[sentence_index] == sentence_reqs.get(sub_sentence):
                    continue
                # If there is a requirement for this atomic sentence, but it doesn't fit
                else:
                    break
            # If the type of `sentence` is `Sentence`, it is not an atomic sentence, and we use recursion to drill
            # one level deeper.
            elif type(sub_sentence) == Sentence:
                sub_sentence.test_value_possible(truth_value_combo[sentence_index])
            # If it's not either of the types, something is wrong
            else:
                raise Exception("Incorrect sentence type: " + str(type(sub_sentence)))

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
