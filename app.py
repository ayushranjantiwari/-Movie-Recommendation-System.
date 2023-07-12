import streamlit as st 
import pandas as pd
import pickle
import requests

def fetch(movie_index):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_index}?api_key=ac365d2a65f2d7477cbce1316692d878&language=en-USlanguage=en-US')
    data = response.json()
    return "https://image.tmdb.org/t/p/w500" + data["poster_path"]

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distance = similarity[movie_index]
    movies_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x : x[1])[1:6]
    recommended_movies = []
    recommended_movies_poster = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch(movie_id))
    return recommended_movies, recommended_movies_poster

movies_list = pickle.load(open('movie_model.pkl', 'rb'))
movies = pd.DataFrame(movies_list)
similarity = pickle.load(open('similarity_movie.pkl', 'rb'))

st.title('Movie Recommendation System')

selected_movie_name = st.selectbox(
    'Choose the movie', movies['title'].values
)

if st.button('recommend'):
    name, poster = recommend(selected_movie_name)
    col1 , col2, col3, col4, col5 = st.columns(5)

    with col1: 
        st.text(name[0])
        st.image(poster[0])
    with col2: 
        st.text(name[1])
        st.image(poster[1])
    with col3: 
        st.text(name[2])
        st.image(poster[2])
    with col4: 
        st.text(name[3])
        st.image(poster[3])
    with col5:
        st.text(name[4])
        st.image(poster[4])

