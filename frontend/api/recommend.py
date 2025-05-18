from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np
from pathlib import Path
import traceback

app = Flask(__name__)
CORS(app)

# Load the model
model_path = Path(__file__).parent.parent / 'movie_recommender.joblib'
try:
    print(f"Looking for model at: {model_path}")
    model = joblib.load(model_path)
    print("Model loaded successfully")
except Exception as e:
    print(f"Error loading model: {str(e)}")
    print(f"Stack trace: {traceback.format_exc()}")
    model = None

@app.route('/recommend', methods=['POST'])
def get_recommendations():
    try:
        print("Received recommendation request")
        data = request.json
        print(f"Request data: {data}")
        
        genres = data.get('genres', [])
        runtime = data.get('runtime', 'medium')
        age = data.get('age', 25)
        
        print(f"Processing request with genres={genres}, runtime={runtime}, age={age}")
        
        if model is None:
            print("Model not loaded, returning error")
            return jsonify({
                "success": False,
                "error": "Model not loaded"
            }), 500
        
        # Get recommendations from model
        print("Making prediction with model")
        input_data = np.array([[genres, runtime, age]])
        print(f"Model input: {input_data}")
        
        recommendations = model.predict(input_data)
        print(f"Got recommendations: {recommendations}")
        
        # Format recommendations
        formatted_recommendations = [
            {
                'title': rec['title'],
                'year': rec['year'],
                'genres': rec['genres'],
                'runtime': rec['runtime'],
                'rating': rec['rating'],
                'tagline': rec['tagline']
            }
            for rec in recommendations[:5]
        ]
        
        print(f"Returning {len(formatted_recommendations)} recommendations")
        return jsonify({
            "success": True,
            "recommendations": formatted_recommendations
        })
        
    except Exception as e:
        print(f"Error in get_recommendations: {str(e)}")
        print(f"Stack trace: {traceback.format_exc()}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

if __name__ == '__main__':
    print("Starting Flask server on port 3000...")
    app.run(port=3000, debug=True) 