from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import os
import numpy as np
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Load the model
model_path = '../movie_recommender.joblib'
model = joblib.load(model_path)

@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        genres = data.get('genres', [])
        runtime = data.get('runtime', 'medium')  # short, medium, long
        age = data.get('age', 25)

        # Process the input data according to your model's requirements
        # This is a placeholder - adjust according to your actual model's input requirements
        input_data = {
            'genres': genres,
            'runtime': runtime,
            'age': age
        }

        # Get predictions from the model
        recommendations = model.predict([input_data])  # Adjust according to your model's predict method

        # Format the response
        response = {
            'recommendations': recommendations.tolist() if isinstance(recommendations, np.ndarray) else recommendations,
            'status': 'success'
        }

        return jsonify(response)

    except Exception as e:
        return jsonify({'error': str(e), 'status': 'error'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000) 