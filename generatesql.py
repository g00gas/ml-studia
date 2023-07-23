
import pandas as pd

def create_sql_file():
    ratings_data = pd.read_csv('ml-latest-small/ratings.csv')
    movies_data = pd.read_csv('ml-latest-small/movies.csv')
    links_data = pd.read_csv('ml-latest-small/links.csv')


    movies_data[['title', 'year']] = movies_data['title'].str.extract(r'^(.*?)\s\((\d{4})\)$')

    sql_statements = []

    for _, row in ratings_data.iterrows():
        sql = f"INSERT INTO ratings (userId, movieId, rating) VALUES ({row['userId']}, {row['movieId']}, {row['rating']});"
        sql_statements.append(sql)

    for _, row in movies_data.iterrows():
        title = row['title'] if not pd.isna(row['title']) else 'Unknown Movie'
        title = title.replace("'", "''")  # Handle single quotes in movie titles
        sql = f"INSERT INTO movies (movieId, title, genres, year) VALUES ({row['movieId']}, '{title}', '{row['genres']}', {row['year']});"
        sql_statements.append(sql)

    for _, row in links_data.iterrows():
        sql = f"INSERT INTO links (movieId, imdbId, tmdbId) VALUES ({row['movieId']}, {row['imdbId']}, {row['tmdbId']});"
        sql_statements.append(sql)

    with open('movie_data.sql', 'w') as file:
        for sql in sql_statements:
            file.write(sql + '\n')

if __name__ == "__main__":
    create_sql_file()