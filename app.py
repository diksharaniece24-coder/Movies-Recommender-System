import streamlit as st
import pickle
import requests

def fetch_poster(movie_id):
    try:
        url='https://api.themoviedb.org/3/movie/{}?api_key=e39b78284a7702e32b5dca4dede9dce6'.format(movie_id)
        response=requests.get(url,timeout=10)
        data=response.json()
        if data.get('poster_path'):
            return "https://image.tmdb.org/t/p/w500/"+data['poster_path']
        else:
            return None
    except:
        return None

def recommend(movie):
    movie_index=movies_list[movies_list['title']==movie].index[0]
    distances=similarity[movie_index]
    movies=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]

    recommended_movies=[]
    recommended_posters=[]

    for i in movies:
        movie_id=movies_list.iloc[i[0]].id
        recommended_movies.append(movies_list.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))

    return recommended_movies,recommended_posters

movies_list=pickle.load(open('movies.pkl','rb'))
movie_titles=movies_list['title'].values
similarity=pickle.load(open('similarity.pkl','rb'))

st.title('Movie Recommender System')

selected_movie_name=st.selectbox(
    'How would you like to be contacted?',
    movie_titles
)

if st.button('Recommend'):
    recommendations,posters=recommend(selected_movie_name)

    cols=st.columns(5)

    for i in range(len(recommendations)):
        with cols[i]:
            st.write(recommendations[i])
            if posters[i]:
                st.image(posters[i],width=150)