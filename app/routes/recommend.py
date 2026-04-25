from fastapi import APIRouter, HTTPException

from app.models.schema import RecommendRequest, RecommendResponse
from app.services.recommender import (
    MovieNotFoundError,
    RecommenderDataError,
    get_all_movie_titles,
    recommend_movies,
)

router = APIRouter()


@router.get("/movies")
def get_movies():
    try:
        return {"movies": get_all_movie_titles()}
    except RecommenderDataError as error:
        raise HTTPException(status_code=500, detail=str(error))


@router.post("/recommend", response_model=RecommendResponse)
def recommend(request: RecommendRequest):
    try:
        recommendations = recommend_movies(request.movie_name)

        return {
            "movie_name": request.movie_name,
            "recommendations": recommendations,
        }

    except MovieNotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error))

    except RecommenderDataError as error:
        raise HTTPException(status_code=500, detail=str(error))
