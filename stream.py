import pickle
import streamlit as st
import requests

# 🔁 Fetch poster from TMDB
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get('poster_path')
    if poster_path:
        return "https://image.tmdb.org/t/p/w500/" + poster_path
    else:
        return "https://via.placeholder.com/500x750.png?text=No+Image"

# 🎯 Recommend using similarity + rating + popularity
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = list(enumerate(similarity[index]))
    distances = sorted(distances, reverse=True, key=lambda x: x[1])

    movie_list = []
    for i in distances[1:11]:  # Top 10
        title = movies.iloc[i[0]].title
        rating = movies.iloc[i[0]]['vote_average']
        popularity = movies.iloc[i[0]]['popularity']
        movie_id = movies.iloc[i[0]]['movie_id']
        movie_list.append((title, rating, popularity, movie_id))

    sorted_movies = sorted(movie_list, reverse=True, key=lambda x: (x[1], x[2]))

    recommended_names = []
    recommended_posters = []

    for title, _, _, movie_id in sorted_movies[:5]:
        recommended_names.append(title)
        recommended_posters.append(fetch_poster(movie_id))

    return recommended_names, recommended_posters

# 🔀 Recommend from same cluster
def recommend_by_cluster(movie):
    index = movies[movies['title'] == movie].index[0]
    cluster = movies.iloc[index]['cluster']
    similar_movies = movies[(movies['cluster'] == cluster) & (movies.index != index)]

    recommended_names = []
    recommended_posters = []

    for i, row in similar_movies.sample(min(5, len(similar_movies))).iterrows():
        recommended_names.append(row['title'])
        recommended_posters.append(fetch_poster(row['movie_id']))

    return recommended_names, recommended_posters

# 🖥️ Streamlit App
st.header('Movie Recommender System')

# Load models
movies = pickle.load(open('model/movie_list.pkl', 'rb'))
similarity = pickle.load(open('model/similarity.pkl', 'rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

# 🔘 Button 1 - Similarity Recommendation
if st.button('Show Recommendation'):
    names, posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])

# 🔘 Button 2 - Cluster Recommendation
if st.button('Cluster-Based Recommendation'):
    names, posters = recommend_by_cluster(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])
