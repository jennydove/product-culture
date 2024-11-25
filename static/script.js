document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('voting-form');
    const resetBtn = document.getElementById('reset-btn');
    const submitBtn = document.getElementById('submit-btn');
    const currentAverage = document.getElementById('current-average');
    const message = document.getElementById('message');
    const resultsContainer = document.getElementById('results-container');
    const resultsContent = document.getElementById('results-content');
    
    let scores = {};

    // Initialize sliders and update scores
    document.querySelectorAll('.slider').forEach(slider => {
        const scoreSpan = slider.nextElementSibling;
        slider.addEventListener('input', function() {
            scoreSpan.textContent = this.value;
            scores[this.id] = parseFloat(this.value);
            updateAverage();
        });
    });

    // Update average score
    function updateAverage() {
        const values = Object.values(scores);
        const avg = values.length ? values.reduce((a, b) => a + b) / values.length : 0;
        currentAverage.textContent = avg.toFixed(2);
    }

    // Reset all sliders
    resetBtn.addEventListener('click', function() {
        document.querySelectorAll('.slider').forEach(slider => {
            slider.value = 0;
            slider.nextElementSibling.textContent = '0';
        });
        scores = {};
        updateAverage();
    });

    // Submit scores
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        fetch('/submit_scores', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ scores: scores }),
        })
        .then(response => response.json())
        .then(data => {
            console.log('Received data:', data);
            if (data.success) {
                message.textContent = data.message;
                message.className = 'success';
                displayResults(data);
            } else {
                message.textContent = data.message;
                message.className = 'error';
            }
            message.classList.remove('hidden');
        })
        .catch(error => {
            console.error('Error:', error);
            message.textContent = 'An error occurred. Please try again.';
            message.className = 'error';
            message.classList.remove('hidden');
        });
    });

    // Display results
    function displayResults(data) {
        if (!data || !data.individual_scores || !data.averages) {
            console.error('Invalid data received:', data);
            message.textContent = 'Error displaying results. Please try again.';
            message.className = 'error';
            message.classList.remove('hidden');
            return;
        }
        resultsContent.innerHTML = '';
        for (const [term, scores] of Object.entries(data.individual_scores)) {
            const resultGroup = document.createElement('div');
            resultGroup.className = 'result-group';
            resultGroup.innerHTML = `
                <h3>${term}</h3>
                <div class="result-line">
                    <div class="vote-dots"></div>
                    <div class="average-marker" style="left: ${(data.averages[term] + 2) / 4 * 100}%"></div>
                </div>
                <span class="average-score">Average: ${data.averages[term].toFixed(2)}</span>
            `;
            const voteDots = resultGroup.querySelector('.vote-dots');
            scores.forEach(score => {
                const dot = document.createElement('div');
                dot.className = 'dot';
                dot.style.left = `${(score + 2) / 4 * 100}%`;
                voteDots.appendChild(dot);
            });
            resultsContent.appendChild(resultGroup);
        }
        resultsContainer.classList.remove('hidden');
    }
});