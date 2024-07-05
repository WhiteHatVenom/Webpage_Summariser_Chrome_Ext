from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import pipeline
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

summariser = pipeline("summarization")

def extract_and_summarize(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    results = soup.find_all(['h1', 'h2', 'h3', 'p'])
    text = [result.text for result in results]
    article = ' '.join(text)
    article = article.replace('.', '.<eos>')
    article = article.replace('?', '?<eos>')
    article = article.replace('!', '!<eos>')
    sentences = article.split('<eos>')
    max_chunk = 500
    curr_chunk = 0
    chunks = []

    for sentence in sentences:
        if len(chunks) == curr_chunk + 1:
            if len(chunks[curr_chunk]) + len(sentence.split(' ')) <= max_chunk:
                chunks[curr_chunk].extend(sentence.split(' '))
            else:
                curr_chunk += 1
                chunks.append(sentence.split(' '))
        else:
            chunks.append(sentence.split(' '))

    for chunk_id in range(len(chunks)):
        chunks[chunk_id] = ' '.join(chunks[chunk_id])

    res = summariser(chunks, max_length=120, min_length=30, do_sample=False)
    summary = ' '.join([summ['summary_text'] for summ in res])

    return summary

@app.route('/summarize', methods=['POST'])
def summarize():
    data = request.json
    url = data['url']
    print(url)
    summary = extract_and_summarize(url)
    print(summary)
    return jsonify({'summary': summary})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
