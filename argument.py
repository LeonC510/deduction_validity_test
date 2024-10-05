import sentence


class Argument:
    def __init__(self, premises: list[sentence], conclusion: sentence):
        self.premises = premises
        self.conclusion = conclusion

    def get_all_sentences(self):
        return self.premises + [self.conclusion]