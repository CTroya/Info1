class DFA:
    def __init__(self, transitions, allStates, fStates):
        self.transitions = transitions
        self.allStates = allStates
        self.fStates = fStates

    def to_dict(self):
        return {
            'transitions': self.transitions,
            'allStates': self.allStates,
            'fStates': self.fStates
        }
