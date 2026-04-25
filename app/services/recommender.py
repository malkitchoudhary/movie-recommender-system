from difflib import get_close_matches

import numpy as np
import pandas as pd
import requests
from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor

from app.utils.loader import DataLoadError, load_recommender_data


TMDB_API_KEY = "8265bd1679663a7ea12ac168da84d2e8"
POSTER_PLACEHOLDER = "https://via.placeholder.com/500x750?text=No+Poster"


class MovieNotFoundError(Exception):
    pass


class RecommenderDataError(Exception):
    pass


@lru_cache(maxsize=3000)
def fetch_poster(movie_id):
    try:
        url = (
            f"https://api.themoviedb.org/3/movie/{movie_id}"
            f"?api_key={TMDB_API_KEY}&language=en-US"
        )

        response = requests.get(url, timeout=3)
        response.raise_for_status()

        data = response.json()
        poster_path = data.get("poster_path")

        if not poster_path:
            return POSTER_PLACEHOLDER

        return "https://image.tmdb.org/t/p/w500" + poster_path

    except Exception:
        return POSTER_PLACEHOLDER



def get_movie_titles(movies):
    if not isinstance(movies, pd.DataFrame):
        raise RecommenderDataError("movie_list.pkl must contain a pandas DataFrame.")

    if "title" not in movies.columns:
        raise RecommenderDataError("movie_list.pkl must contain a 'title' column.")

    return movies["title"].astype(str).tolist()


def find_movie_index(movie_name, movie_titles):
    search_name = movie_name.strip().lower()

    # Exact match
    for index, title in enumerate(movie_titles):
        if title.strip().lower() == search_name:
            return index

    # Partial match
    for index, title in enumerate(movie_titles):
        if search_name in title.strip().lower():
            return index

    # Fuzzy match for spelling mistakes
    suggestions = get_close_matches(movie_name, movie_titles, n=1, cutoff=0.45)

    if suggestions:
        matched_movie = suggestions[0]

        for index, title in enumerate(movie_titles):
            if title == matched_movie:
                return index

    raise MovieNotFoundError(
        f"Movie '{movie_name}' not found in dataset. Please type another movie name."
    )


def recommend_movies(movie_name, limit=5):
    try:
        movies, similarity = load_recommender_data()
    except DataLoadError as error:
        raise RecommenderDataError(str(error))

    movie_titles = get_movie_titles(movies)
    movie_index = find_movie_index(movie_name, movie_titles)

    similarity_matrix = np.asarray(similarity)

    distances = sorted(
        list(enumerate(similarity_matrix[movie_index])),
        reverse=True,
        key=lambda item: item[1],
    )

    selected_movies = []

    for index, score in distances[1 : limit + 1]:
        movie_title = movies.iloc[index]["title"]

        if "movie_id" in movies.columns:
            movie_id = int(movies.iloc[index]["movie_id"])
        else:
            movie_id = None

        selected_movies.append(
            {
                "title": movie_title,
                "movie_id": movie_id,
            }
        )

    movie_ids = [movie["movie_id"] for movie in selected_movies]

    with ThreadPoolExecutor(max_workers=5) as executor:
        poster_urls = list(executor.map(fetch_poster, movie_ids))

    recommendations = []

    for movie, poster_url in zip(selected_movies, poster_urls):
        recommendations.append(
            {
                "title": movie["title"],
                "poster_url": poster_url,
            }
        )

    return recommendations

def get_all_movie_titles():
    try:
        movies, similarity = load_recommender_data()
    except DataLoadError as error:
        raise RecommenderDataError(str(error))

    return get_movie_titles(movies)

