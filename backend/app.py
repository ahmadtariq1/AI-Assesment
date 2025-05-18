from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
from sklearn.metrics.pairwise import cosine_similarity
import os

app = Flask(__name__)
CORS(app)

# Load the model
model_path = os.path.join(os.path.dirname(__file__), 'movie_recommender.joblib')

def recommend_movies(genre_preference, runtime_pref, age, top_n=5, min_rating=8.0):
    """
    Recommend movies based on genre preference, runtime preference, and age
    """
    try:
        # Load the model
        model = joblib.load(model_path)
        tfidf = model['tfidf']
        cosine_sim = model['cosine_sim']
        movies = model['movies']
        
        # Determine age rating based on user's age
        if age < 10:
            age_rating = 'all'
        elif 10 <= age < 13:
            age_rating = '10+'
        elif 13 <= age < 17:
            age_rating = '13+'
        else:
            age_rating = '17+'
        
        # Clean genre input
        cleaned_genre = ' '.join([g.strip().lower() for g in genre_preference.split(',')])
        
        # Create query string
        query = f"{cleaned_genre} {runtime_pref.lower()} {age_rating}"
        
        # Vectorize the query
        query_vec = tfidf.transform([query])
        
        # Compute similarity between query and all movies
        sim_scores = cosine_similarity(query_vec, tfidf.transform(model['features'])).flatten()
        
        # Filter movies by minimum rating and age appropriateness
        valid_movies = movies[
            (movies['rating'] >= min_rating) & 
            (movies['age_rating'] <= age_rating)
        ].copy()
        valid_movies['similarity'] = sim_scores[valid_movies.index]
        
        # Get top N most similar movies
        recommendations = valid_movies.sort_values(
            by=['similarity', 'rating'], 
            ascending=[False, False]
        ).head(top_n)
        
        # Prepare output
        return recommendations[['name', 'year', 'genre', 'rating', 'runtime_category', 'tagline']].to_dict('records')
    except Exception as e:
        print(f"Error in recommend_movies: {str(e)}")
        return []

@app.route('/api/recommend', methods=['POST'])
def get_recommendations():
    try:
        data = request.json
        genre_preference = data.get('genres', '')
        runtime_pref = data.get('runtime', 'medium')
        age = int(data.get('age', 18))
        
        recommendations = recommend_movies(
            genre_preference=genre_preference,
            runtime_pref=runtime_pref,
            age=age
        )
        
        return jsonify({
            'success': True,
            'recommendations': recommendations
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True) 