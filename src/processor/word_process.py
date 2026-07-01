from sudachipy import dictionary, tokenizer
import re


tokenizer_obj = dictionary.Dictionary(dict="full").create()
mode = tokenizer.Tokenizer.SplitMode.C

def sudachi_tokenize(text):
    if not text or not isinstance(text, str): return ""
    text = re.sub(r'[\s\u3000]+', '', text)

    sentences = [s for s in re.split(r'(?<=。)', text) if s]
    all_nouns = []

    for sentence in sentences:
        try:
            tokens = tokenizer_obj.tokenize(sentence, mode)
            nouns = [m.surface() for m in tokens if m.part_of_speech()[0] == "名詞" and len(m.surface()) > 1]
            all_nouns.extend(nouns)
        except Exception:
            continue

    return " ".join(all_nouns)



