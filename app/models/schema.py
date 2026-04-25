from typing import List

from pydantic import BaseModel, Field


class RecommendRequest(BaseModel):
    movie_name: str = Field(..., min_length=1)


class MovieRecommendation(BaseModel):
    title: str
    poster_url: str


class RecommendResponse(BaseModel):
    movie_name: str
    recommendations: List[MovieRecommendation]
