import os
import joblib
from sklearn.pipeline import Pipeline as SklearnPipeline

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))

tag_rating_model_path = os.path.join(project_root, 'models', 'tag_rating_model.pkl')
tag_rating_model: SklearnPipeline = joblib.load(tag_rating_model_path)