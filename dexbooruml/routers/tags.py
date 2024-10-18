import joblib
import os
import dexbooruml.utilities as utilities
from fastapi import APIRouter
from pydantic import BaseModel
from sklearn.pipeline import Pipeline as SklearnPipeline
from dexbooruml.utilities.tags import normalize_tags


class TagRatingInput(BaseModel):
    tags: list[str]

def register_endpoints(router: APIRouter):
    @router.post('/rating')     
    def predict_post_rating_from_tags(model_input: TagRatingInput):
        input_tags = model_input.tags
        normalized_tag_sentence = normalize_tags(nlp=utilities.nlp, input_tags=input_tags)

        prediction = utilities.tag_rating_model.predict([normalized_tag_sentence])    
        predicted_rating = prediction[0]

        return {
            'predicted_rating': predicted_rating,
            'input_tags': input_tags,
        }


def build_tag_router() -> tuple[APIRouter, str]:   
    router = APIRouter()    
    register_endpoints(router)

    return router, 'tags'