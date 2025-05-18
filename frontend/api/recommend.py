from http.server import BaseHTTPRequestHandler
import json
import os
import joblib
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

# Load the model
model_path = os.path.join(os.path.dirname(__file__), '..', 'movie_recommender.joblib')
recommender = joblib.load(model_path)

# Sample movies (you should replace these with your actual movie data)
sample_movies = [
    {
        "title": "The Shawshank Redemption",
        "genres": ["Drama"],
        "rating": 9.3,
        "runtime": 142,
        "description": "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency."
    },
    {
        "title": "Inception",
        "genres": ["Action", "Adventure", "Sci-Fi"],
        "rating": 8.8,
        "runtime": 148,
        "description": "A thief who steals corporate secrets through dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O."
    }
]

def get_recommendations(genres, runtime, age):
    try:
        # Filter by runtime
        runtime_filters = {
            'short': lambda x: x['runtime'] < 90,
            'medium': lambda x: 90 <= x['runtime'] <= 120,
            'long': lambda x: x['runtime'] > 120
        }
        
        filtered_movies = [
            movie for movie in sample_movies 
            if (not genres or any(g in movie['genres'] for g in genres))
            and (not runtime or runtime_filters[runtime](movie))
        ]
        
        return filtered_movies
    except Exception as e:
        print(f"Error in get_recommendations: {str(e)}")
        return []

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)
        
        genres = data.get('genres', [])
        runtime = data.get('runtime', 'medium')
        age = data.get('age', 25)
        
        recommendations = get_recommendations(genres, runtime, age)
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        response = {
            'success': True,
            'recommendations': recommendations
        }
        
        self.wfile.write(json.dumps(response).encode())
        
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers() 