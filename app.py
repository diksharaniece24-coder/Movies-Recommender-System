import streamlit as st
import pickle
import requests
import gdown
import os

# ── Download similarity.pkl from Google Drive if not present ──────────────────

@st.cache_resource
def load_data():
    if not os.path.exists('similarity.pkl'):
        with st.spinner('Downloading similarity matrix (one-time setup)...'):
            file_id = '10eWAhUqTilcsgUiFAHDUwEyI9-M1o58R'
            gdown.download(
                id=file_id,
                output='similarity.pkl',
                quiet=False
            )
    movies = pickle.load(open('movies.pkl', 'rb'))
    similarity = pickle.load(open('similarity.pkl', 'rb'))
    return movies, similarity

movies_list, similarity = load_data()
movie_titles = movies_list['title'].values

# ── Fetch movie poster from TMDB ──────────────────────────────────────────────
def fetch_poster(movie_id):
    try:
        url = 'https://api.themoviedb.org/3/movie/{}?api_key=e39b78284a7702e32b5dca4dede9dce6'.format(movie_id)
        response = requests.get(url, timeout=10)
        data = response.json()
        if data.get('poster_path'):
            return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
        return None
    except:
        return None

# ── Recommendation logic ──────────────────────────────────────────────────────
def recommend(movie):
    movie_index = movies_list[movies_list['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []
    for i in movies:
        movie_id = movies_list.iloc[i[0]].id
        recommended_movies.append(movies_list.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_posters

# ── UI ────────────────────────────────────────────────────────────────────────
st.title('Movie Recommender System')

selected_movie_name = st.selectbox('Select a movie:', movie_titles)

if st.button('Recommend'):
    recommendations, posters = recommend(selected_movie_name)
    cols = st.columns(5)
    for i in range(len(recommendations)):
        with cols[i]:
            st.write(recommendations[i])
            if posters[i]:
                st.image(posters[i], width=150)

