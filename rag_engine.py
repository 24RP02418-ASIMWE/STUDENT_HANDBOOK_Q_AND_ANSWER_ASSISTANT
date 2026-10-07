from pathlib import Path
import re
import numpy as np
from pypdf import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

PDF_PATH = Path('data/school_handbook.pdf')

def load_handbook():
    if not PDF_PATH.exists():
        raise FileNotFoundError('school_handbook.pdf was not found inside data/.')
    reader = PdfReader(str(PDF_PATH))
    pages = []
    for page_number, page in enumerate(reader.pages, start=1):
        text = re.sub(r'\s+', ' ', page.extract_text() or '').strip()
        if text:
            pages.append({'page': page_number, 'text': text})
    return pages

def chunk_pages(pages, words_per_chunk=180, overlap=40):
    chunks = []
    for page in pages:
        words = page['text'].split()
        if len(words) <= words_per_chunk:
            chunks.append({'page': page['page'], 'text': page['text']})
            continue
        start = 0
        while start < len(words):
            end = min(start + words_per_chunk, len(words))
            chunks.append({'page': page['page'], 'text': ' '.join(words[start:end])})
            if end == len(words):
                break
            start = end - overlap
    return chunks

def retrieve(question, top_k=4):
    chunks = chunk_pages(load_handbook())
    documents = [c['text'] for c in chunks]
    vectorizer = TfidfVectorizer(lowercase=True, stop_words='english', ngram_range=(1, 2))
    matrix = vectorizer.fit_transform(documents)
    query_vector = vectorizer.transform([question])
    scores = cosine_similarity(query_vector, matrix).flatten()
    indexes = np.argsort(scores)[::-1][:top_k]
    return [{'page': chunks[i]['page'], 'text': chunks[i]['text'], 'score': float(scores[i])} for i in indexes]

def extractive_answer(question, retrieved):
    if not retrieved or retrieved[0]['score'] < 0.08:
        return 'I could not find enough relevant information in the RP Student Handbook to answer this question.'
    context = ' '.join(item['text'] for item in retrieved)
    qwords = {w.lower() for w in re.findall(r'[A-Za-z0-9]+', question) if len(w) > 2}
    sentences = re.split(r'(?<=[.!?])\s+', context)
    ranked = []
    for sentence in sentences:
        words = {w.lower() for w in re.findall(r'[A-Za-z0-9]+', sentence)}
        overlap = len(qwords.intersection(words))
        if overlap:
            ranked.append((overlap, sentence))
    ranked.sort(key=lambda x: x[0], reverse=True)
    return ' '.join(s for _, s in ranked[:4]) if ranked else (sentences[0] if sentences else context)

def answer_question(question):
    retrieved = retrieve(question)
    return {'answer': extractive_answer(question, retrieved), 'retrieved': retrieved, 'sources': [{'page': x['page'], 'score': x['score']} for x in retrieved]}
