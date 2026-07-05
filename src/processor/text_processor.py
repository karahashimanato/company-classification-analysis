import numpy as np
import pandas as pd

def chunk_text_by_sentence(text, max_chars=800):

    if not isinstance(text, str) or not text.strip():
        return []

    raw_sentences = text.split("。")
    sentences = [s.strip() + "。" for s in raw_sentences if s.strip()]
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(sentence) > max_chars:
            if current_chunk:
                chunks.append(current_chunk)
                current_chunk = ""
            for i in range(0, len(sentence), max_chars):
                chunks.append(sentence[i:i+max_chars])
            continue

        if len(current_chunk) + len(sentence) > max_chars:
            chunks.append(current_chunk)
            current_chunk = sentence
        else:
            current_chunk += sentence

    if current_chunk:
        chunks.append(current_chunk)

    return chunks