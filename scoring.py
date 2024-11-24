from collections import Counter

scores = []

def store_score(score):
    scores.append(score)

def get_all_scores():
    counter = Counter(scores)
    return {
        'L': counter['L'],
        'M': counter['M'],
        'H': counter['H'],
        'total': len(scores)
    }