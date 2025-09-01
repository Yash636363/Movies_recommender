import streamlit as st
import pickle
import pandas as pd
import requests
import io

# -------------------------------
# Function to rejoin similarity.pkl parts
# -------------------------------
def load_similarity():
    buffer = io.BytesIO()
    for i in range(8):  # Change this if you have more/less parts
        with open(f'similarity.pkl_part{i}', 'rb') as f:
            buffer.write(f.read())
    buffer.seek(0)
    return pickle.load(buffer)

# -------------------------------
# Function to fetch movie poster
# -------------------------------
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path
# -------------------------------
# Recommendation Logic
# -------------------------------
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(
        list(enumerate(distances)), reverse=True, key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))
    
    return recommended_movies, recommended_posters

# -------------------------------
# Load Data
# -------------------------------
st.title("🎬 Movie Recommender System")

# Load movie dictionary
movies_dict = pickle.load(open('movie_list.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

# Load similarity data from split files
similarity = load_similarity()

# -------------------------------
# UI
# -------------------------------
selected_movie_name = st.selectbox(
    "Select a movie to get recommendations:",
    movies['title'].values
)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])