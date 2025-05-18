import { useState } from 'react';
import {
  Box,
  Container,
  Typography,
  Paper,
  Grid,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  TextField,
  Button,
  Card,
  CardContent,
  CardMedia,
  FormControlLabel,
  Radio,
  RadioGroup,
  CircularProgress,
  Alert,
  Fade,
} from '@mui/material';
import type { SelectChangeEvent } from '@mui/material/Select';

const genres = [
  'Action', 'Adventure', 'Animation', 'Comedy', 'Crime',
  'Documentary', 'Drama', 'Family', 'Fantasy', 'Horror',
  'Mystery', 'Romance', 'Sci-Fi', 'Thriller'
];

interface Movie {
  name: string;
  year: number;
  genre: string;
  rating: number;
  runtime_category: string;
  tagline: string;
}

export default function MovieRecommender() {
  const [selectedGenres, setSelectedGenres] = useState<string[]>([]);
  const [runtime, setRuntime] = useState('medium');
  const [age, setAge] = useState('');
  const [recommendations, setRecommendations] = useState<Movie[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleGenreChange = (event: SelectChangeEvent<string[]>) => {
    setSelectedGenres(event.target.value as string[]);
  };

  const handleRuntimeChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setRuntime(event.target.value);
  };

  const handleAgeChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setAge(event.target.value);
  };

  const handleSubmit = async () => {
    if (!selectedGenres.length || !age) {
      setError('Please select at least one genre and enter your age');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const response = await fetch('/api/recommend', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          genres: selectedGenres.join(', '),
          runtime,
          age: parseInt(age),
        }),
      });

      const data = await response.json();

      if (!data.success) {
        throw new Error(data.error || 'Failed to get recommendations');
      }

      setRecommendations(data.recommendations);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Typography variant="h3" component="h1" gutterBottom align="center" sx={{ mb: 4 }}>
        Movie Recommendations
      </Typography>

      <Paper elevation={3} sx={{ p: 3, mb: 4 }}>
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <FormControl fullWidth>
              <InputLabel>Genres</InputLabel>
              <Select
                multiple
                value={selectedGenres}
                onChange={handleGenreChange}
                label="Genres"
              >
                {genres.map((genre) => (
                  <MenuItem key={genre} value={genre}>
                    {genre}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>

          <Grid item xs={12} md={6}>
            <FormControl fullWidth>
              <Typography component="legend">Runtime Preference</Typography>
              <RadioGroup row value={runtime} onChange={handleRuntimeChange}>
                <FormControlLabel
                  value="short"
                  control={<Radio />}
                  label="Short (<90m)"
                />
                <FormControlLabel
                  value="medium"
                  control={<Radio />}
                  label="Medium (90-150m)"
                />
                <FormControlLabel
                  value="long"
                  control={<Radio />}
                  label="Long (>150m)"
                />
              </RadioGroup>
            </FormControl>
          </Grid>

          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              type="number"
              label="Your Age"
              value={age}
              onChange={handleAgeChange}
              inputProps={{ min: 1, max: 100 }}
            />
          </Grid>

          <Grid item xs={12}>
            <Button
              variant="contained"
              color="primary"
              size="large"
              onClick={handleSubmit}
              disabled={loading}
              fullWidth
            >
              {loading ? <CircularProgress size={24} color="inherit" /> : 'Get Recommendations'}
            </Button>
          </Grid>
        </Grid>
      </Paper>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      <Grid container spacing={3}>
        {recommendations.map((movie, index) => (
          <Fade in={true} key={index} style={{ transitionDelay: `${index * 100}ms` }}>
            <Grid item xs={12} sm={6} md={4}>
              <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
                <CardMedia
                  component="img"
                  height="200"
                  image={`https://picsum.photos/seed/${movie.name}/400/200`}
                  alt={movie.name}
                  sx={{ objectFit: 'cover' }}
                />
                <CardContent sx={{ flexGrow: 1 }}>
                  <Typography gutterBottom variant="h6" component="h2">
                    {movie.name} ({movie.year})
                  </Typography>
                  <Typography variant="body2" color="text.secondary" paragraph>
                    {movie.genre}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    IMDb: {movie.rating.toFixed(1)} | Runtime: {movie.runtime_category}
                  </Typography>
                  {movie.tagline && (
                    <Typography variant="body2" sx={{ mt: 1, fontStyle: 'italic' }}>
                      "{movie.tagline}"
                    </Typography>
                  )}
                </CardContent>
              </Card>
            </Grid>
          </Fade>
        ))}
      </Grid>
    </Container>
  );
} 