from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
import logging
from typing import List, Dict

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Load the movies data
try:
    movies_path = os.path.join(os.path.dirname(__file__), 'movies.json')
    logger.info(f"Loading movies from: {movies_path}")
    with open(movies_path, 'r') as f:
        movies_data = json.load(f)
    logger.info("Movies data loaded successfully")
except Exception as e:
    logger.error(f"Error loading movies data: {str(e)}")
    movies_data = {"movies": []}

def filter_movies(genres: List[str], runtime: str, age: int) -> List[Dict]:
    """Filter movies based on user preferences."""
    runtime_ranges = {
        'short': (0, 90),
        'medium': (90, 150),
        'long': (150, float('inf'))
    }
    
    runtime_min, runtime_max = runtime_ranges.get(runtime, (90, 150))
    
    filtered_movies = []
    for movie in movies_data['movies']:
        # Check if any of the selected genres match the movie's genres
        if any(genre in movie['genres'] for genre in genres):
            # Check if runtime is within the selected range
            if runtime_min <= movie['runtime'] <= runtime_max:
                filtered_movies.append(movie)
    
    # Sort by rating and return top 5
    return sorted(filtered_movies, key=lambda x: x['rating'], reverse=True)[:5]

@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        logger.info(f"Received request data: {data}")

        genres = data.get('genres', [])
        runtime = data.get('runtime', 'medium')
        age = data.get('age', 25)

        if not genres:
            return jsonify({'error': 'At least one genre must be selected', 'status': 'error'}), 400

        # Get movie recommendations
        recommendations = filter_movies(genres, runtime, age)
        
        if not recommendations:
            return jsonify({
                'error': 'No movies found matching your criteria',
                'status': 'error'
            }), 404

        response = {
            'recommendations': recommendations,
            'status': 'success'
        }

        logger.info(f"Sending response with {len(recommendations)} recommendations")
        return jsonify(response)

    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return jsonify({'error': str(e), 'status': 'error'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000) 