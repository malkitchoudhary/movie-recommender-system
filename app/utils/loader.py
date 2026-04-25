import pickle
from functools import lru_cache
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"

MOVIE_LIST_PATH = DATA_DIR / "movie_list.pkl"
SIMILARITY_PATH = DATA_DIR / "similarity.pkl"


class DataLoadError(Exception):
    pass


def load_pickle_file(file_path):
    if not file_path.exists():
        raise DataLoadError(f"File not found: {file_path}")

    try:
        with open(file_path, "rb") as file:
            return pickle.load(file)
    except Exception as error:
        raise DataLoadError(f"Could not load file: {file_path}. Error: {error}")


@lru_cache(maxsize=1)
def load_recommender_data():
    movies = load_pickle_file(MOVIE_LIST_PATH)
    similarity = load_pickle_file(SIMILARITY_PATH)

    return movies, similarity
