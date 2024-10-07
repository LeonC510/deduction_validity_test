import argument


def test_validity(test_argument: argument):
    atomic_sentences = set()
    atomic_sentences_truth_values = dict()
    all_sentences = test_argument.get_all_sentences()
    for sentence in all_sentences:
        sentence.get_atomic_sentences(atomic_sentences)

    # Convert the `atomic_sentences` set into a dictionary
    for atomic_sentence in atomic_sentences:
        atomic_sentences_truth_values.update({atomic_sentence: True})
    # Standing requirements for atomic sentences
    sentence_reqs = dict()

    for i in range(3):
        (conclusion_possible, new_sentence_reqs) = test_argument.conclusion.test_value_possible(True, sentence_reqs)
        print("This conclusion is " + str(conclusion_possible) + " possible")
        print("Sentence requirements:" + str(new_sentence_reqs))
