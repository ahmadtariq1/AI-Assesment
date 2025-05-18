import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib

# Create sample movie data
movies_data = {
    'name': [
        'The Shawshank Redemption', 'The Godfather', 'Pulp Fiction',
        'The Dark Knight', 'Forrest Gump', 'The Matrix',
        'Inception', 'Goodfellas', 'The Silence of the Lambs',
        'Fight Club'
    ],
    'year': [1994, 1972, 1994, 2008, 1994, 1999, 2010, 1990, 1991, 1999],
    'genre': [
        'Drama', 'Crime, Drama', 'Crime, Drama',
        'Action, Crime, Drama', 'Drama, Romance', 'Action, Sci-Fi',
        'Action, Adventure, Sci-Fi', 'Biography, Crime, Drama',
        'Crime, Drama, Thriller', 'Drama'
    ],
    'rating': [9.3, 9.2, 8.9, 9.0, 8.8, 8.7, 8.8, 8.7, 8.6, 8.8],
    'runtime_category': [
        'long', 'long', 'medium',
        'medium', 'medium', 'medium',
        'medium', 'medium', 'medium',
        'medium'
    ],
    'age_rating': [
        '17+', '17+', '17+',
        '13+', '13+', '13+',
        '13+', '17+', '17+',
        '17+'
    ],
    'tagline': [
        'Fear can hold you prisoner. Hope can set you free.',
        'An offer you can\'t refuse.',
        'You won\'t know the facts until you\'ve seen the fiction.',
        'Why so serious?',
        'Life is like a box of chocolates...',
        'Welcome to the Real World',
        'Your mind is the scene of the crime',
        'As far back as I can remember, I always wanted to be a gangster.',
        'To enter the mind of a killer she must challenge the mind of a madman.',
        'Mischief. Mayhem. Soap.'
    ]
}

# Create DataFrame
movies = pd.DataFrame(movies_data)

# Create features for similarity calculation
movies['features'] = movies.apply(
    lambda x: f"{x['genre'].lower()} {x['runtime_category']} {x['age_rating']}",
    axis=1
)

# Create TF-IDF vectorizer
tfidf = TfidfVectorizer(stop_words='english')
features_matrix = tfidf.fit_transform(movies['features'])

# Calculate cosine similarity
cosine_sim = features_matrix

# Save the model
model_data = {
    'tfidf': tfidf,
    'cosine_sim': cosine_sim,
    'movies': movies,
    'features': movies['features']
}

joblib.dump(model_data, 'movie_recommender.joblib')
print("Sample model created successfully!") 