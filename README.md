# Movie Recommendation System

A modern web application that provides personalized movie recommendations based on user preferences including genres, runtime, and age preferences.

## Features

- React/TypeScript frontend with Material-UI components
- Flask backend with machine learning-based recommendation system
- Dark theme with modern UI/UX
- Real-time recommendations
- Responsive design

## Project Structure

```
.
├── frontend/           # React TypeScript frontend
├── backend/           # Flask Python backend
└── movie_recommender.joblib  # Pre-trained recommendation model
```

## Setup Instructions

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The frontend will be available at `http://localhost:5173`

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt
python app/main.py
```

The backend API will be available at `http://localhost:3001`

## Environment Variables

Create a `.env` file in the frontend directory:

```
VITE_API_URL=http://localhost:3001
```

## Deployment

### Frontend (Vercel)

The frontend is ready for Vercel deployment. Connect your GitHub repository to Vercel and it will automatically detect the React/Vite configuration.

### Backend

The backend requires a Python environment with the dependencies listed in `requirements.txt`.

## Tech Stack

- Frontend:
  - React
  - TypeScript
  - Material-UI
  - Framer Motion
  - Vite

- Backend:
  - Flask
  - scikit-learn
  - Python

## License

MIT 