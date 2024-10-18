import re
from spacy.language import Language

ACCEPTED_POS = ['NOUN', 'PROPN', 'VERB', 'ADJ']
BLACKLISTED_SUBSTRINGS = ['res', 'artist', 'character', 'unknown']

def replace_special_characters(target: str) -> str:
    return re.sub(r'[^a-zA-Z0-9\s]', '', target).lower().strip()

def normalize_tags(nlp: Language, input_tags: list[str]) -> str:
    normalized_tokens = []  
    input_tag_sentence = replace_special_characters(' '.join(input_tags))
    document = nlp(text=input_tag_sentence)
        
    for token in document:
        token_lemma = token.lemma_.lower().strip()
        if not token.is_stop and all(word not in token_lemma for word in BLACKLISTED_SUBSTRINGS) and token.pos_ in ACCEPTED_POS:
            normalized_tokens.append(token_lemma)
    
    return ' '.join(normalized_tokens)