import argument


class validity_tester:
    def __init__(self, test_argument: argument):
        self.test_argument = test_argument

        atomic_sentences = set()
        self.atomic_sentences_truth_values = dict()
        all_sentences = self.test_argument.get_all_sentences()
        for sentence in all_sentences:
            sentence.get_atomic_sentences(atomic_sentences)
        print(atomic_sentences)
        # Convert the `atomic_sentences` set into a dictionary
        for atomic_sentence in atomic_sentences:
            self.atomic_sentences_truth_values.update({atomic_sentence: True})
        # Standing requirements for atomic sentences
        self.sentence_reqs = dict()

