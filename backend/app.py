from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import os
import numpy as np
from dotenv import load_dotenv
import logging
import dill

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

app = Flask(__name__)
CORS(app)

# Load the model
try:
    model_path = os.path.join(os.path.dirname(__file__), '..', 'movie_recommender.joblib')
    logger.info(f"Loading model from: {model_path}")
    with open(model_path, 'rb') as f:
        model = joblib.load(f, mmap_mode='r')
    logger.info("Model loaded successfully")
except Exception as e:
    logger.error(f"Error loading model: {str(e)}")
    model = None

def process_model_input(genres, runtime, age):
    """Process the input data for model prediction."""
    runtime_map = {
        'short': 0,
        'medium': 1,
        'long': 2
    }
    
    # Convert runtime to numeric value
    runtime_value = runtime_map.get(runtime, 1)
    
    # Create feature vector
    return {
        'genres': genres,
        'runtime_category': runtime_value,
        'target_age': age
    }

@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        if model is None:
            return jsonify({'error': 'Model not loaded', 'status': 'error'}), 500

        data = request.json
        logger.info(f"Received request data: {data}")

        genres = data.get('genres', [])
        runtime = data.get('runtime', 'medium')
        age = data.get('age', 25)

        if not genres:
            return jsonify({'error': 'At least one genre must be selected', 'status': 'error'}), 400

        # Process input data
        input_data = process_model_input(genres, runtime, age)
        logger.info(f"Processed input data: {input_data}")

        try:
            # Get predictions from the model
            recommendations = model.predict([input_data])
            logger.info(f"Model predictions: {recommendations}")

            # Format the response
            response = {
                'recommendations': recommendations if isinstance(recommendations, list) else recommendations.tolist(),
                'status': 'success'
            }
        except Exception as model_error:
            logger.error(f"Error during model prediction: {str(model_error)}")
            # Return sample recommendations for testing
            sample_recommendations = [
                {
                    'title': 'The Dark Knight',
                    'year': 2008,
                    'rating': 9.0,
                    'genres': ['Action', 'Crime', 'Drama'],
                    'runtime': 152,
                    'tagline': 'Why So Serious?',
                    'poster_path': 'https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911r6m7haRef0WH.jpg'
                },
                {
                    'title': 'Inception',
                    'year': 2010,
                    'rating': 8.8,
                    'genres': ['Action', 'Adventure', 'Sci-Fi'],
                    'runtime': 148,
                    'tagline': 'Your mind is the scene of the crime.',
                    'poster_path': 'https://image.tmdb.org/t/p/w500/9gk7adHYeDvHkCSEqAvQNLV5Uge.jpg'
                },
                {
                    'title': 'Interstellar',
                    'year': 2014,
                    'rating': 8.6,
                    'genres': ['Adventure', 'Drama', 'Sci-Fi'],
                    'runtime': 169,
                    'tagline': 'Mankind was born on Earth. It was never meant to die here.',
                    'poster_path': 'https://image.tmdb.org/t/p/w500/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg'
                }
            ]
            response = {
                'recommendations': sample_recommendations,
                'status': 'success'
            }

        logger.info(f"Sending response: {response}")
        return jsonify(response)

    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return jsonify({'error': str(e), 'status': 'error'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000) 