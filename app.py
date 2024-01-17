import pickle
import streamlit as st
import requests


def fetch_movie_details(movie_id):
    api_key = "8265bd1679663a7ea12ac168da84d2e8"
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return {
            'poster_path': data['poster_path'],
            'release_date': data['release_date'],
            'rating': data['vote_average'],
        }
    else:
        st.error(f"Failed to fetch movie details for Movie ID: {movie_id}")
        return None


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movies = []

    for i in distances[1:6]:
        # fetch the movie details
        movie_id = movies.iloc[i[0]].movie_id
        movie_details = fetch_movie_details(movie_id)

        if movie_details:
            # add movie details to the recommendation list
            recommended_movies.append({
                'name': movies.iloc[i[0]].title,
                'poster': fetch_poster(movie_details['poster_path']),
                'release_date': movie_details['release_date'],
                'rating': movie_details['rating'],
            })

    return recommended_movies


# Streamlit UI
st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="wide"
)


def fetch_poster(poster_path):
    full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
    return full_path


st.header('🍿 Movie Recommender System')
movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movies = recommend(selected_movie)

    for movie in recommended_movies:
        st.text(movie['name'])
        st.text(f"Release Date: {movie['release_date']}")
        st.text(f"Rating: {movie['rating']}")
        st.image(movie['poster'])

    # Add a divider
    st.markdown("---")

    # Add a thank you message
    st.success("🎉 Enjoy your movie recommendations!")