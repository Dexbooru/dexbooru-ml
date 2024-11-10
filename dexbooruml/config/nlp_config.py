import spacy
import os
from dotenv import load_dotenv

load_dotenv()

nlp = spacy.load(os.getenv('SPACY_MODEL_NAME', 'en_core_web_md'))
