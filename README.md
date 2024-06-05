# Sentiment Analysis API

This project is a simple sentiment analysis API built using FastAPI. The API takes input text and returns the probabilities of the text being positive or negative using a pre-trained DistilBERT model fine-tuned on the SST-2 dataset.

## Features

- Sentiment analysis using the DistilBERT model.
- Returns probabilities for positive and negative sentiments.

## Requirements

- Python 3.8+
- FastAPI
- Transformers
- Torch

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/sentiment-analysis-api.git
    cd sentiment-analysis-api
    ```

2. Create and activate a virtual environment:
    ```bash
    python -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Run the FastAPI server:
    ```bash
    uvicorn main:app --reload
    ```

2. The API will be available at `http://127.0.0.1:8000`.

3. To analyze sentiment, send a POST request to `/sentiment-analysis/` with a JSON payload containing the input text:
    ```json
    {
        "inputs": "I like you"
    }
    ```

4. The response will be a JSON array with the probabilities of the text being positive or negative:
    ```json
    [
        [
            {
                "label": "POSITIVE",
                "score": 0.9998695850372314
            },
            {
                "label": "NEGATIVE",
                "score": 0.00013043530634604394
            }
        ]
    ]
    ```

## Example

Example POST request using `curl`:
```bash
curl -X POST "http://127.0.0.1:8000/sentiment-analysis/" -H "Content-Type: application/json" -d '{"inputs": "I like you"}'
