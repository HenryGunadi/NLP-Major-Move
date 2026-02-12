# NLP Major Move – Multi-Task FinBERT

Multi-task fine-tuning of FinBERT to jointly model:

- Financial news sentiment (classification)
- Article importance (classification)

The model uses a shared transformer backbone with task-specific heads and is evaluated using macro and weighted F1 metrics.

---

## Installation

```bash
pip install -r requirements.txt
```

A virtual environment is recommended. GPU is recommended for training.

---

## Training

Training is implemented in:

```
ml/notebooks/FinBERT_MultiTask.ipynb
```

Trained model weights are not included due to GitHub size limitations.  
After training, save the model locally and update the model path where necessary.

---

## Data Source

Financial news data is retrieved using the **MarketAux API**.

Base endpoint used:

```
https://api.marketaux.com/v1/news/all
```

---

## Running the Backend Server

1. Inside the `server/` directory, create a `.env` file:

```
NEWS_API_TOKEN=your_token_here
NEWS_API_BASE_URL=https://api.marketaux.com/v1/news/all
```

2. From the root directory, run:

```bash
python server/main.py
```

Ensure the trained model path is correctly configured in the server code.

---

## Running the Frontend

No frontend framework or Node server is used.

To run the frontend:

- Open the HTML file using a Live Server extension (e.g., VS Code Live Server),  
  or  
- Open the HTML file directly in your browser.

---

## Notes

- Model weights are excluded due to size constraints.
- Adjust local paths before running.
- GPU recommended for training.
