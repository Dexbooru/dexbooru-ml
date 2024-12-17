import spacy
import os
from dotenv import load_dotenv

load_dotenv()

_nlp = None

def get_nlp():
    global _nlp
    if _nlp is None:
        _nlp = spacy.load(os.getenv('SPACY_MODEL_NAME', 'en_core_web_md'))
    return _nlp

nlp = get_nlp()
