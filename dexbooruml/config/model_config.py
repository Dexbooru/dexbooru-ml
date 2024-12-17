import os
import joblib
from typing import Union
from sklearn.pipeline import Pipeline as SklearnPipeline

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
tag_rating_model_path = os.path.join(project_root, 'models', 'tag_rating_model.pkl')
_tag_rating_model: Union[SklearnPipeline, None] = None

def get_tag_rating_model():
    global _tag_rating_model

    if _tag_rating_model is None:
        _tag_rating_model = joblib.load(tag_rating_model_path)
    
    return _tag_rating_model

tag_rating_model = get_tag_rating_model()
