from flask import Flask, render_template, request, jsonify, flash
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from scoring import store_score, get_all_scores

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a real secret key

# Set up rate limiting
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        score = request.form.get('score')
        if score in ['L', 'M', 'H']:
            store_score(score)
            flash('Score submitted successfully!', 'success')
        else:
            flash('Invalid score. Please choose L, M, or H.', 'error')
    
    scores = get_all_scores()
    return render_template('index.html', scores=scores)

@app.route('/submit_score', methods=['POST'])
@limiter.limit("10 per minute")
def submit_score():
    score = request.form.get('score')
    if score in ['L', 'M', 'H']:
        store_score(score)
        scores = get_all_scores()
        return jsonify({'success': True, 'message': 'Score submitted successfully!', 'scores': scores})
    else:
        return jsonify({'success': False, 'message': 'Invalid score. Please choose L, M, or H.'})

if __name__ == '__main__':
    app.run(debug=True)