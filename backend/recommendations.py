import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.neighbors import NearestNeighbors
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import psycopg2


connection = psycopg2.connect(
        host="localhost",
        database="movie_recommendations",
        user="postgres",
        password="haslo123", 
        port=5432
    )
get_ratings_query = pd.read_sql_query (
    '''
                               SELECT
                               *
                               FROM ratings
                               ''', 
    connection)
get_movies_query = pd.read_sql_query ('''
                               SELECT
                               *
                               FROM movies
                               ''', connection)
get_links_query = pd.read_sql_query ('''
                               SELECT
                               *
                               FROM links
                               ''', connection)

def collaborative_filtering_reccomendation(user_id_to_find_recommendations_for, n_neighbors=10, top_recommendations=10):
    # Assuming you have already loaded the 'ratings.csv' and 'movies.csv'
    ratings_data = get_ratings_query
    # Step 1: Prepare the data and create user-item matrix
    user_item_matrix = ratings_data.pivot(index='userid', columns='movieid', values='rating').fillna(0)

    # Step 2: Choose a collaborative filtering algorithm (k-Nearest Neighbors)
    knn_model = NearestNeighbors(n_neighbors=n_neighbors, metric='cosine', algorithm='brute')
    knn_model.fit(user_item_matrix.values)

    # Step 3: Make movie recommendations for the specified user
    user_index = user_item_matrix.index.get_loc(user_id_to_find_recommendations_for)
    user_ratings = user_item_matrix.iloc[user_index].values

    # Step 4: Find the nearest neighbors (similar users) to the target user
    user_ratings_reshaped = user_ratings.reshape(1, -1)  # Reshape to a 2D array with one row
    _, indices = knn_model.kneighbors(user_ratings_reshaped)

    # Step 5: Get movie recommendations based on similar users' preferences
    similar_users_indices = indices.squeeze()
    recommendations = user_item_matrix.iloc[similar_users_indices].mean(axis=0)
    sorted_recommendations = recommendations.sort_values(ascending=False)

    # Print the top movie recommendations
    recommended_movies = sorted_recommendations.head(top_recommendations)
    return recommended_movies


def content_based_recommendation(movie_title_to_find_recommendations_for, top_recommendations=10):
    # Załóżmy, że dane 'movies.csv' zostały już załadowane
    movies_data = get_movies_query

    # Krok 1: Przygotuj dane i stwórz macierz TF-IDF dla tytułów i gatunków filmów
    tfidf_vectorizer = TfidfVectorizer(stop_words='english', use_idf=True)
    tfidf_matrix_titles = tfidf_vectorizer.fit_transform(movies_data['title'])
    tfidf_matrix_genres = tfidf_vectorizer.fit_transform(movies_data['genres'].fillna(''))

    # Oblicz podobieństwo kosinusowe pomiędzy tytułami filmów
    cosine_similarities_titles = linear_kernel(tfidf_matrix_titles, tfidf_matrix_titles)

    # Oblicz podobieństwo kosinusowe pomiędzy gatunkami filmów
    cosine_similarities_genres = linear_kernel(tfidf_matrix_genres, tfidf_matrix_genres)

    # Znajdź indeks filmu, dla którego chcemy dokonać rekomendacji
    movie_index = movies_data.index[movies_data['title'] == movie_title_to_find_recommendations_for].tolist()[0]

    # Uzyskaj oceny podobieństwa (podobne tytuły filmów) dla danego filmu
    similar_titles_indices = cosine_similarities_titles[movie_index].argsort()[::-1][1:]
    similar_genres_indices = cosine_similarities_genres[movie_index].argsort()[::-1][1:]

    # Łącz podobne filmy na podstawie tytułów i gatunków
    combined_indices = list(set(similar_titles_indices[:top_recommendations]) | set(similar_genres_indices[:top_recommendations]))

    # Wyświetl rekomendacje filmów na podstawie treści (tytułów i gatunków)
    recommended_movies = movies_data.iloc[combined_indices][:top_recommendations]
    return recommended_movies