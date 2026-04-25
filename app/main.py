from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.recommend import router as recommend_router

app = FastAPI(
    title="Movie Recommender System",
    description="Movie recommendation API using precomputed pickle files",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "Movie Recommender System API is running"}


app.include_router(recommend_router)
