# scoring.py
from collections import defaultdict

class VotingResults:
    def __init__(self):
        self.scores = defaultdict(list)  # {term: [list of scores]}
        self.averages = {}  # {term: average_score}

    def store_score(self, term, score):
        self.scores[term].append(float(score))
        self.averages[term] = sum(self.scores[term]) / len(self.scores[term])

    def get_all_scores(self):
        return {
            'individual_scores': dict(self.scores),
            'averages': self.averages
        }
    
# Create a global instance
voting_results = VotingResults()

def store_score(term, score):
    voting_results.store_score(term, score)

def get_all_scores():
    return voting_results.get_all_scores()