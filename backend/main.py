# app.py

from flask import Flask, jsonify, request
from recommendations import collaborative_filtering_reccomendation, content_based_recommendation
import psycopg2

app = Flask(__name__)

def get_movie_data():
    connection = psycopg2.connect(
        host="localhost",
        database="movie_recommendations",
        user="postgres",
        password="haslo123",
        port=5432
    )
    cursor = connection.cursor()

    cursor.execute('SELECT links.movieId, title, year, imdbId, ARRAY_AGG(ratings.userId) as users '
                   'FROM links '
                   'LEFT JOIN movies ON links.movieId = movies.movieId '
                   'LEFT JOIN ratings ON links.movieId = ratings.movieId '
                    'GROUP BY links.movieId, title, year, imdbId')  
    movies = []
    for row in cursor.fetchall():
        movie_info = {
            'movieId': row[0],
            'title': row[1],
            'year': row[2],
            'imdbId': row[3],  # Adding imdbId to the dictionary
            'users': [int(user_id) for user_id in row[4] if user_id]
        }
        movies.append(movie_info)

    cursor.close()
    connection.close()
    
    return movies

@app.route('/api/movies', methods=['GET'])
def get_movies():
    movies = get_movie_data()
    return jsonify(movies)


@app.route('/api/cfr', methods=['POST'])
def get_recommendations():
    request_data = request.get_json()

    user_id = int(request_data.get('user_id'))
    n_neighbors = int(request_data.get('n_neighbors', 10))
    top_recommendations = int(request_data.get('top_recommendations', 10))

    recommendations = collaborative_filtering_reccomendation(user_id, n_neighbors, top_recommendations)
    recommended_movies = [{
        'movie_title': movie_id,
        'predicted_rating': rating
    } for movie_id, rating in recommendations.items()]

    return jsonify(recommended_movies)


@app.route('/api/cbr', methods=['POST'])
def get_content_recommendations():
    request_data = request.get_json()

    movie_title = request_data.get('movie_title')
    top_recommendations = int(request_data.get('top_recommendations', 10))

    recommendations = content_based_recommendation(movie_title, top_recommendations)
    recommended_movies = [{
        'movieid': row['movieid'],
        'title': row['title'],
        'year': row['year'],
        'genres': row['genres']
    } for _, row in recommendations.iterrows()]

    return jsonify(recommended_movies)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)