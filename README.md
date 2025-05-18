# Movie Recommendation App

A modern web application that suggests movies based on genre, runtime, and age preferences using a pre-trained machine learning model.

## Features

- Multi-select genre filtering
- Runtime preference selection (Short/Medium/Long)
- Age-based recommendations
- Modern, responsive UI with dark theme
- Smooth animations and transitions
- Movie cards with posters, ratings, and details

## Tech Stack

- Frontend:
  - React with TypeScript
  - Material-UI for components
  - Framer Motion for animations
  - React Query for API calls
  - Vite for build tooling

- Backend:
  - Flask API
  - scikit-learn for ML model
  - CORS support
  - Environment variable configuration

## Local Development

1. Clone the repository:
```bash
git clone <repository-url>
cd movie-recommendation-app
```

2. Set up the frontend:
```bash
cd frontend
npm install
npm run dev
```

3. Set up the backend:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

4. Open http://localhost:5173 in your browser

## Deployment

The application is configured for deployment on Vercel:

1. Push your code to GitHub
2. Import the repository in Vercel
3. Configure the following environment variables in Vercel:
   - `PYTHON_VERSION`: 3.13
   - Any other environment variables needed by your application

## Project Structure

```
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/    # React components
│   │   └── App.tsx       # Main application
│   ├── package.json
│   └── vite.config.ts
├── backend/               # Flask backend
│   ├── app.py            # Main Flask application
│   └── requirements.txt   # Python dependencies
├── movie_recommender.joblib  # Pre-trained ML model
└── vercel.json           # Vercel deployment config
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request 