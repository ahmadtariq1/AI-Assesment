from http.server import BaseHTTPRequestHandler
import json
import os

# Sample movies database
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
    },
    {
        "title": "The Dark Knight",
        "genres": ["Action", "Crime", "Drama"],
        "rating": 9.0,
        "runtime": 152,
        "description": "When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice."
    },
    {
        "title": "Pulp Fiction",
        "genres": ["Crime", "Drama"],
        "rating": 8.9,
        "runtime": 154,
        "description": "The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine in four tales of violence and redemption."
    },
    {
        "title": "Toy Story",
        "genres": ["Animation", "Adventure", "Comedy"],
        "rating": 8.3,
        "runtime": 81,
        "description": "A cowboy doll is profoundly threatened and jealous when a new spaceman figure supplants him as top toy in a boy's room."
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
        
        # Filter movies based on genres and runtime
        filtered_movies = [
            movie for movie in sample_movies 
            if (not genres or any(g in movie['genres'] for g in genres))
            and (not runtime or runtime_filters[runtime](movie))
        ]
        
        # Sort by rating
        filtered_movies.sort(key=lambda x: x['rating'], reverse=True)
        
        return filtered_movies[:5]  # Return top 5 movies
    except Exception as e:
        print(f"Error in get_recommendations: {str(e)}")
        return []

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
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
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({
                'success': False,
                'error': str(e)
            }).encode())
        
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers() 