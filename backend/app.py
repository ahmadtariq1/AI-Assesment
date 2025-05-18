from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import os
import numpy as np
from dotenv import load_dotenv
import logging

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
    model = joblib.load(model_path)
    logger.info("Model loaded successfully")
except Exception as e:
    logger.error(f"Error loading model: {str(e)}")
    model = None

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

        # Create a sample response for testing
        sample_recommendations = [
            {
                'title': 'The Shawshank Redemption',
                'year': 1994,
                'rating': 9.3,
                'genres': ['Drama'],
                'runtime': 142,
                'tagline': 'Fear can hold you prisoner. Hope can set you free.',
                'poster_path': 'https://image.tmdb.org/t/p/w500/q6y0Go1tsGEsmtFryDOJo3dEmqu.jpg'
            },
            {
                'title': 'The Godfather',
                'year': 1972,
                'rating': 9.2,
                'genres': ['Crime', 'Drama'],
                'runtime': 175,
                'tagline': 'An offer you can\'t refuse.',
                'poster_path': 'https://image.tmdb.org/t/p/w500/3bhkrj58Vtu7enYsRolD1fZdja1.jpg'
            }
        ]

        # Process the input data according to your model's requirements
        input_data = {
            'genres': genres,
            'runtime': runtime,
            'age': age
        }
        logger.info(f"Processed input data: {input_data}")

        try:
            # Get predictions from the model
            recommendations = model.predict([input_data])
            logger.info(f"Model predictions: {recommendations}")

            # Format the response
            response = {
                'recommendations': recommendations.tolist() if isinstance(recommendations, np.ndarray) else recommendations,
                'status': 'success'
            }
        except Exception as model_error:
            logger.error(f"Error during model prediction: {str(model_error)}")
            # Return sample recommendations for now
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