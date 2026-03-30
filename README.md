# LLMArena — Multi-LLM Research Paper Extraction Benchmarker

> Benchmark Gemini vs Llama 3 on extracting structured data from academic PDFs

## What it does
- Extracts 13 structured fields from any research paper PDF
- Benchmarks Gemini 2.5 Flash vs Llama 3 (Groq) on accuracy, speed and cost
- RAG pipeline using ChromaDB — ask natural language questions across papers
- Streamlit dashboard with leaderboard, charts and Q&A viewer

## Results
| Model | Accuracy | Latency | Cost |
|-------|----------|---------|------|
| Llama 3 (Groq) | 100% | 0.86s | Free |
| Gemini 2.5 Flash | 100% | 12.79s | $0.0007 |

## Tech stack
Python 3.11 · PyMuPDF · Groq · Gemini · ChromaDB · Pydantic · Streamlit

## Run locally
```bash
pip install -r requirements.txt
jupyter notebook LLMArena.ipynb
streamlit run dashboard.py
```

## Key finding
Llama 3 via Groq is 14.9x faster than Gemini and completely free — with identical accuracy.