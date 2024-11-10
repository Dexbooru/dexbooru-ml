import joblib
import os
from fastapi import APIRouter
from pydantic import BaseModel
from sklearn.pipeline import Pipeline as SklearnPipeline
from dexbooruml.utilities.tags import normalize_tags
from dexbooruml.config.model_config import tag_rating_model

class TagRatingInput(BaseModel):
    tags: list[str]

def register_endpoints(router: APIRouter):
    @router.post('/rating')     
    def predict_post_rating_from_tags(model_input: TagRatingInput):
        input_tags = model_input.tags
        normalized_tag_sentence = normalize_tags(input_tags=input_tags)

        prediction = tag_rating_model.predict([normalized_tag_sentence])    
        predicted_rating = prediction[0]

        return {
            'status': 'success',
            'predicted_rating': predicted_rating,
            'input_tags': input_tags,
        }


def build_tag_router() -> tuple[APIRouter, str]:   
    router = APIRouter()    
    register_endpoints(router)

    return router, 'tags'