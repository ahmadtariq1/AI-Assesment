# Movie Recommendation App

A modern web application that recommends movies based on user preferences using a pre-trained machine learning model.

## Features

- Genre-based movie recommendations
- Runtime preference filtering
- Age-appropriate suggestions
- Modern, Netflix-inspired UI
- Responsive design

## Tech Stack

- Frontend: React + TypeScript + Vite
- UI Framework: Material-UI
- Backend: Flask
- ML Model: Scikit-learn (pre-trained)
- Deployment: Vercel

## Setup

### Prerequisites

- Node.js (v14 or higher)
- Python (v3.8 or higher)
- Git

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

### Development

1. Start the backend server (will run on http://localhost:5000)
2. Start the frontend development server (will run on http://localhost:5173)
3. The frontend will proxy API requests to the backend automatically

### Deployment

The app is configured for deployment on Vercel:

1. Push your changes to GitHub
2. Connect your repository to Vercel
3. Vercel will automatically deploy both frontend and backend

## Model Usage

The movie recommendation model (`movie_recommender.joblib`) uses the following parameters:

- Genre preferences (multiple selections allowed)
- Runtime preference (short/medium/long)
- User's age (for age-appropriate recommendations)

The model returns the top 5 movie recommendations based on these preferences.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request 