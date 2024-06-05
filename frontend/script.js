document.getElementById('submitBtn').addEventListener('click', async () => {
    const inputText = document.getElementById('inputText').value;
    const response = await fetch('http://127.0.0.1:8000/sentiment-analysis/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ inputs: inputText })
    });

    if (response.ok) {
        const result = await response.json();
        displayResult(result);
    } else {
        alert('Error: ' + response.statusText);
    }
});

function displayResult(result) {
    const resultContainer = document.getElementById('result');
    resultContainer.innerHTML = '';

    const positiveResult = result[0].find(r => r.label === 'POSITIVE');
    const negativeResult = result[0].find(r => r.label === 'NEGATIVE');

    const positiveDiv = document.createElement('div');
    positiveDiv.className = 'positive';
    positiveDiv.innerHTML = `<i class="fas fa-smile-beam"></i> POSITIVE: ${(positiveResult.score * 100).toFixed(2)}%`;

    const negativeDiv = document.createElement('div');
    negativeDiv.className = 'negative';
    negativeDiv.innerHTML = `<i class="fas fa-sad-tear"></i> NEGATIVE: ${(negativeResult.score * 100).toFixed(2)}%`;

    resultContainer.appendChild(positiveDiv);
    resultContainer.appendChild(negativeDiv);
}
