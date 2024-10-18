import pandas as pd
import spacy
import os
import json
import ast
import re
import multiprocessing
from spacy.tokens import Doc as Document
from tqdm import tqdm

ACCEPTED_POS = ['NOUN', 'PROPN', 'VERB', 'ADJ']
BLACKLISTED_SUBSTRINGS = ['res', 'artist', 'character', 'unknown']

def process_posts(file_path: str):
    print(f'Processing the file under: {file_path}')
    
    posts = []
    with open(file_path, 'r') as file:
        lines = file.read().splitlines()

    for line in tqdm(lines):
        post = json.loads(line)
        tags = [tag['name'] for tag in post['tags']]
        
        processed_post = {
            'tags': tags,
            'rating': post['rating']
        }
        posts.append(processed_post)

    return posts


def replace_special_characters(target: str) -> str:
    return re.sub(r'[^a-zA-Z0-9\s]', '', target)

def normalize_tag_doc(document: Document) -> str:
    normalized_tokens = []

    for token in document:
        token_lemma = token.lemma_.lower().strip()
        if not token.is_stop and all(word not in token_lemma for word in BLACKLISTED_SUBSTRINGS) and token.pos_ in ACCEPTED_POS:
            normalized_tokens.append(token_lemma)
    
    return ' '.join(normalized_tokens)



def main():
    nlp = spacy.load('en_core_web_md', exclude=['tok2vec'])
    posts_folder_path = '../data/danbooru_posts'
    json_files = [filename for filename in os.listdir(posts_folder_path) if filename.endswith('.json')]

    dataframes = []

    for json_file in json_files:
        file_path = os.path.join(posts_folder_path, json_file)
        posts = process_posts(file_path)

        dataframe = pd.DataFrame.from_records(posts)
        dataframes.append(dataframe)

    danbooru_df = pd.concat(dataframes, axis=0)
    danbooru_df['tags'] = danbooru_df['tags'].apply(lambda raw_tag_str: replace_special_characters(' '.join(ast.literal_eval(raw_tag_str.lower().strip()))))

    total_posts = danbooru_df.shape[0]
    processed_tags = []
    docs = nlp.pipe(danbooru_df['tags'], n_process=-1)

    for doc in tqdm(docs, total=total_posts):
        processed_tags.append(normalize_tag_doc(doc))

    danbooru_df['tags'] = processed_tags

    danbooru_df.to_csv('../data/danbooru_posts/danbooru_tags.csv', index=False)

if __name__ == '__main__':
    main()