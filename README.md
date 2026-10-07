# RP Student Handbook Q&A Assistant

## Project title
School Student Handbook Question Answering Assistant Using Retrieval-Augmented Generation (RAG)

## Problem
Students may spend time searching through a long student handbook to find rules and procedures.

## Solution
The application accepts a natural-language question, searches the RP Student Handbook, retrieves relevant passages, and returns a grounded answer with handbook page sources.

## Technologies
Python, Streamlit, PyPDF, TF-IDF, cosine similarity, NumPy, and Scikit-learn.

## Run in VS Code (Windows)
1. Open this folder in VS Code.
2. Terminal -> New Terminal.
3. Run: `python -m venv .venv`
4. Run: `.venv\\Scripts\\activate`
5. Run: `pip install -r requirements.txt`
6. Run: `streamlit run app.py`

## Test examples
- What is the minimum class attendance required?
- How much does a replacement student ID cost?
- How early should students arrive for summative assessment?
- What is the late registration fee?
- What are the rules for using phones during class?

## Evaluation
Run `python evaluate.py` to test retrieval on four sample questions.

## Responsible use
The system shows source pages and should not invent rules when the handbook does not provide enough evidence. The official handbook remains the authoritative document.

## Architecture
Student Question -> PDF preprocessing -> Chunking -> TF-IDF retrieval -> Relevant passages -> Grounded answer -> Answer + source page.
