from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
import torch
from torch.nn import Softmax

# Initialize the FastAPI application
app = FastAPI()

# Add middleware to allow all CORS origins, methods, and headers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Load the pre-trained tokenizer and model for sentiment analysis
try:
    tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")
    model = DistilBertForSequenceClassification.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")
except Exception as e:
    raise RuntimeError(f"Error loading model or tokenizer: {str(e)}")

# Define the response model for sentiment analysis results
class SentimentScore(BaseModel):
    label: str
    score: float

@app.post("/sentiment-analysis/", response_model=List[List[SentimentScore]])
async def analyze_sentiment(input_data: Dict[str, str]) -> List[List[SentimentScore]]:
    try:
        # Retrieve input text from JSON request
        input_text = input_data.get("inputs", "")
        if not input_text:
            raise HTTPException(status_code=400, detail="Input text is required")

        # Tokenize the input text
        inputs = tokenizer(input_text, return_tensors="pt", truncation=True, padding=True)

        # Perform model inference
        with torch.no_grad():
            logits = model(**inputs).logits

        # Apply softmax to convert logits to probabilities
        softmax = Softmax(dim=1)
        probs = softmax(logits).squeeze().tolist()

        # Extract positive and negative probabilities
        positive_prob = float(probs[model.config.label2id["POSITIVE"]])
        negative_prob = float(probs[model.config.label2id["NEGATIVE"]])

        # Format the response
        response = [
            [{"label": "POSITIVE", "score": positive_prob}, {"label": "NEGATIVE", "score": negative_prob}]
        ]

        return response

    except KeyError as e:
        raise HTTPException(status_code=500, detail=f"Label key error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
