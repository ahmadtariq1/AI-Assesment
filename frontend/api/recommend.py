from http.server import BaseHTTPRequestHandler
import json

# Static list of movies
MOVIES = [
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

def handler(request):
    if request.method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            }
        }

    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            genres = body.get('genres', [])
            runtime = body.get('runtime', 'medium')
            
            # Filter movies based on genres and runtime
            recommendations = []
            for movie in MOVIES:
                # Check if any of the selected genres match the movie's genres
                genre_match = not genres or any(g in movie['genres'] for g in genres)
                
                # Check runtime match
                runtime_match = False
                if runtime == 'short' and movie['runtime'] < 90:
                    runtime_match = True
                elif runtime == 'medium' and 90 <= movie['runtime'] <= 150:
                    runtime_match = True
                elif runtime == 'long' and movie['runtime'] > 150:
                    runtime_match = True
                
                if genre_match and runtime_match:
                    recommendations.append(movie)

            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps(recommendations)
            }
            
        except Exception as e:
            return {
                'statusCode': 500,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({'error': str(e)})
            }

    return {
        'statusCode': 405,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({'error': 'Method not allowed'})
    } 