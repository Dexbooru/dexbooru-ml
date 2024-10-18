import pandas as pd
import spacy
import numpy as np
import joblib
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import Pipeline, make_pipeline, FunctionTransformer
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.naive_bayes import MultinomialNB
from tag_classfier_preprocess import replace_special_characters, normalize_tag_doc


def main():
    danbooru_df = pd.read_csv('../data/danbooru_posts/danbooru_tags.csv')
    
    X = danbooru_df['tags']
    y = danbooru_df['rating']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)

    model_pipeline = Pipeline(steps=[
        ('cvect', CountVectorizer()),
        ('gsmnb', MultinomialNB()),
    ])
    
    search_params = {
        'gsmnb__alpha': np.arange(0.0, 1.0, 0.15),
    }
    grid_search = GridSearchCV(estimator=model_pipeline, param_grid=search_params, cv=3, verbose=2, refit=True, n_jobs=3)
    grid_search.fit(X_train, y_train)

    best_model = grid_search.best_estimator_

    joblib.dump(best_model, '../models/tag_rating_classifier.pkl')
    
if __name__ == '__main__':
    main()

