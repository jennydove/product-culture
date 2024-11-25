from flask import Flask, render_template, request, jsonify
from scoring import store_score, get_all_scores
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Default terms
DEFAULT_TERMS = ["Empowered", "Design Savvy", "Technical", "Inspirational", "Lonely", "Powerful"]

@app.route('/', methods=['GET', 'POST'])
def home():
    """
    Render the home page with default terms and their initial scores.

    Returns:
        The rendered template for the home page.
    """
    # Initialize empty scores dictionary with default terms
    scores = {term: 0 for term in DEFAULT_TERMS}
    
    # Render the 'index.html' template with terms and scores
    return render_template('index.html', terms=DEFAULT_TERMS, scores=scores)

@app.route('/submit_scores', methods=['POST'])
def submit_scores():
    data = request.json
    scores = data.get('scores', {})
    
    # Calculate average score
    score_values = [float(v) for v in scores.values()]
    avg_score = sum(score_values) / len(score_values) if score_values else 0

    # Store each score
    for term, score in scores.items():
        store_score(term, float(score))
    
    # Get all scores including the new submission
    all_scores = get_all_scores()

    if not -2 <= avg_score <= 2:
        return jsonify({
            'success': False,
            'message': 'Average score must be between -2 and +2'
        })

    return jsonify({
        'success': True,
        'message': 'Scores submitted successfully',
        'average': round(avg_score, 2),
        'individual_scores': all_scores['individual_scores'],
        'averages': all_scores['averages']
    })

if __name__ == '__main__':
    app.run(debug=True)