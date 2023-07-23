from flask import Flask, jsonify, request
import psycopg2
from flask_cors import CORS
from recommendations import collaborative_filtering_reccomendation, content_based_recommendation
app = Flask(__name__)
CORS(app, origins="*")

connection = psycopg2.connect(
    host="postgres",
    database="movie_recommendations",
    user="postgres",
    password="haslo123",
    port=5432
)

def get_movie_data():
    cursor = connection.cursor()

    cursor.execute('SELECT links.movieId, title, year, imdbId, genres, ARRAY_AGG(ratings.userId) as users '
                   'FROM links '
                   'LEFT JOIN movies ON links.movieId = movies.movieId '
                   'LEFT JOIN ratings ON links.movieId = ratings.movieId '
                    'GROUP BY links.movieId, title, year, imdbId, genres')  
    movies = []
    for row in cursor.fetchall():
        movie_info = {
            'movieId': row[0],
            'title': row[1],
            'year': row[2],
            'imdbId': row[3],
            'genres': row[4],
            'users': [int(user_id) for user_id in row[5] if user_id]
        }
        movies.append(movie_info)

    cursor.close()
    
    return movies

@app.route('/api/movies', methods=['GET'])
def get_movies():
    try:
        movies = get_movie_data()
        return jsonify(movies)
    except psycopg2.Error as e:
        return jsonify({'error': str(e)})

@app.route('/api/cfr', methods=['POST'])
def get_recommendations():
    try:
        request_data = request.get_json()

        user_id = int(request_data.get('user_id'))
        n_neighbors = int(request_data.get('n_neighbors', 10))
        top_recommendations = int(request_data.get('top_recommendations', 10))

        recommendations = collaborative_filtering_reccomendation(user_id, n_neighbors, top_recommendations)

        # Fetch movie details from the movies list based on movieid in recommendations
        movies = get_movie_data()
        recommended_movies = []
        for movie_id, rating in recommendations.items():
            for movie in movies:
                print('movie', movie)
                if movie['movieId'] == movie_id:
                    recommended_movie = {
                        'movieid': movie['movieId'],
                        'title': movie['title'],
                        'year': movie['year'],
                        'genres': movie['genres'],
                        'predicted_rating': rating,
                    }
                    recommended_movies.append(recommended_movie)
                    break  # Break the loop after finding the movie

        return jsonify(recommended_movies)
    except psycopg2.Error as e:
        return jsonify({'error': str(e)})

@app.route('/api/cbr', methods=['POST'])
def get_content_recommendations():
    try:    
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
    except psycopg2.Error as e:
        return jsonify({'error': str(e)})
    
@app.route('/api/users', methods=['GET'])
def get_all_user_ids():
    try:
        cursor = connection.cursor()
        cursor.execute('SELECT DISTINCT userId FROM ratings')
        user_ids = [user_id[0] for user_id in cursor.fetchall()]
        cursor.close()
        users = [{'id': user_id} for user_id in user_ids]
        return jsonify(users)

    except psycopg2.Error as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)