# Movie Recommender System

A FastAPI-based Movie Recommender System using precomputed pickle files.

## Project Description

This project recommends 5 similar movies based on a selected movie name. It uses:

- FastAPI backend
- Pickle files for movie data and similarity matrix
- Vanilla HTML, CSS, and JavaScript frontend

## Required Pickle Files

Place these files inside the `data` folder:

```text
data/movie_list.pkl
data/similarity.pkl
