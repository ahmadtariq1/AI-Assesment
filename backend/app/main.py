from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import os
import numpy as np
from pathlib import Path
import random

app = Flask(__name__)
# Configure CORS to allow requests from frontend
CORS(app, resources={
    r"/*": {  # Allow all routes
        "origins": ["*"],  # Allow all origins
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Sample movie data with simplified information
SAMPLE_MOVIES = [
    {
        "title": "The Shawshank Redemption",
        "genres": ["Drama"],
        "rating": 9.3,
        "description": "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.",
        "runtime": 142
    },
    {
        "title": "Inception",
        "genres": ["Action", "Sci-Fi", "Thriller"],
        "rating": 8.8,
        "description": "A thief who steals corporate secrets through dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.",
        "runtime": 148
    },
    {
        "title": "The Lion King",
        "genres": ["Animation", "Adventure", "Drama"],
        "rating": 8.5,
        "description": "A young lion prince flees his kingdom only to learn the true meaning of responsibility and bravery.",
        "runtime": 88
    },
    {
        "title": "Pulp Fiction",
        "genres": ["Crime", "Drama"],
        "rating": 8.9,
        "description": "The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine in four tales of violence and redemption.",
        "runtime": 154
    },
    {
        "title": "The Dark Knight",
        "genres": ["Action", "Crime", "Drama"],
        "rating": 9.0,
        "description": "When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.",
        "runtime": 152
    }
]

def filter_movies(genres, runtime, age):
    filtered_movies = []
    
    # Convert runtime preferences to approximate minute ranges
    runtime_ranges = {
        'short': (0, 90),
        'medium': (90, 150),
        'long': (150, float('inf'))
    }
    min_runtime, max_runtime = runtime_ranges[runtime]
    
    # Filter movies based on criteria
    for movie in SAMPLE_MOVIES:
        # Check if any of the selected genres match the movie's genres
        if not genres or any(g in movie['genres'] for g in genres):
            # Check runtime
            if min_runtime <= movie['runtime'] <= max_runtime:
                filtered_movies.append(movie)
    
    # Sort by rating and return top movies
    return sorted(filtered_movies, key=lambda x: x['rating'], reverse=True)

@app.route('/api/recommend', methods=['POST'])
def get_recommendations():
    try:
        data = request.json
        print("Received request data:", data)
        genres = data.get('genres', [])
        runtime = data.get('runtime', 'medium')
        age = data.get('age', 25)
        
        print(f"Processing request with genres={genres}, runtime={runtime}, age={age}")
        
        recommendations = filter_movies(genres, runtime, age)
        top_recommendations = recommendations[:5]
        
        print(f"Found {len(top_recommendations)} recommendations")
        
        return jsonify({
            'success': True,
            'recommendations': top_recommendations
        })
    
    except Exception as e:
        print(f"Error in get_recommendations: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    print("Starting Flask server...")
    print(f"Loaded {len(SAMPLE_MOVIES)} sample movies")
    app.run(host='0.0.0.0', debug=True, port=3001) 