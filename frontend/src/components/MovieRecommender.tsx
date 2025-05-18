import { useState } from 'react'
import {
  Box,
  Container,
  Typography,
  Paper,
  Grid,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  RadioGroup,
  Radio,
  FormControlLabel,
  TextField,
  Button,
  Card,
  CardMedia,
  CardContent,
  Rating,
  Chip,
  Stack,
  Alert,
  Snackbar,
} from '@mui/material'
import { motion } from 'framer-motion'
import { useMutation } from '@tanstack/react-query'

const GENRES = [
  'Action', 'Adventure', 'Animation', 'Comedy', 'Crime',
  'Documentary', 'Drama', 'Family', 'Fantasy', 'Horror',
  'Mystery', 'Romance', 'Sci-Fi', 'Thriller'
]

interface MovieRecommendation {
  title: string
  year: number
  rating: number
  genres: string[]
  runtime: number
  tagline: string
  poster_path: string
}

const MovieRecommender = () => {
  const [selectedGenres, setSelectedGenres] = useState<string[]>([])
  const [runtime, setRuntime] = useState('medium')
  const [age, setAge] = useState('25')
  const [recommendations, setRecommendations] = useState<MovieRecommendation[]>([])
  const [error, setError] = useState<string | null>(null)

  const recommendationMutation = useMutation({
    mutationFn: async (data: { genres: string[], runtime: string, age: number }) => {
      console.log('Sending request with data:', data)
      const response = await fetch('/api/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      })
      
      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.error || 'Failed to get recommendations')
      }
      
      const responseData = await response.json()
      console.log('Received response:', responseData)
      
      if (responseData.status === 'error') {
        throw new Error(responseData.error || 'Failed to get recommendations')
      }
      
      return responseData
    },
    onSuccess: (data) => {
      console.log('Setting recommendations:', data.recommendations)
      setRecommendations(data.recommendations)
      setError(null)
    },
    onError: (error: Error) => {
      console.error('Error:', error)
      setError(error.message)
    },
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (selectedGenres.length === 0) {
      setError('Please select at least one genre')
      return
    }
    recommendationMutation.mutate({
      genres: selectedGenres,
      runtime,
      age: parseInt(age),
    })
  }

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Typography variant="h3" component="h1" gutterBottom align="center" sx={{ mb: 4 }}>
        Movie Recommendations
      </Typography>

      <Paper component="form" onSubmit={handleSubmit} sx={{ p: 3, mb: 4 }}>
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <FormControl fullWidth error={selectedGenres.length === 0 && Boolean(error)}>
              <InputLabel>Genres</InputLabel>
              <Select
                multiple
                value={selectedGenres}
                onChange={(e) => {
                  const value = typeof e.target.value === 'string' ? e.target.value.split(',') : e.target.value
                  setSelectedGenres(value)
                  setError(null)
                }}
                label="Genres"
                renderValue={(selected) => (
                  <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                    {selected.map((value) => (
                      <Chip key={value} label={value} />
                    ))}
                  </Box>
                )}
              >
                {GENRES.map((genre) => (
                  <MenuItem key={genre} value={genre}>
                    {genre}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>

          <Grid item xs={12} md={3}>
            <FormControl component="fieldset">
              <Typography variant="subtitle1" gutterBottom>
                Runtime Preference
              </Typography>
              <RadioGroup
                value={runtime}
                onChange={(e) => setRuntime(e.target.value)}
              >
                <FormControlLabel value="short" control={<Radio />} label="Short (<90m)" />
                <FormControlLabel value="medium" control={<Radio />} label="Medium (90-150m)" />
                <FormControlLabel value="long" control={<Radio />} label="Long (>150m)" />
              </RadioGroup>
            </FormControl>
          </Grid>

          <Grid item xs={12} md={3}>
            <TextField
              fullWidth
              label="Age"
              type="number"
              value={age}
              onChange={(e) => setAge(e.target.value)}
              InputProps={{ inputProps: { min: 0, max: 100 } }}
            />
          </Grid>

          <Grid item xs={12}>
            <Button
              fullWidth
              variant="contained"
              size="large"
              type="submit"
              disabled={recommendationMutation.isPending}
            >
              {recommendationMutation.isPending ? 'Getting Recommendations...' : 'Get Recommendations'}
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
          <Grid item xs={12} sm={6} md={4} key={index}>
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
            >
              <Card sx={{ height: '100%' }}>
                <CardMedia
                  component="img"
                  height="300"
                  image={movie.poster_path || 'https://via.placeholder.com/300x450'}
                  alt={movie.title}
                />
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    {movie.title} ({movie.year})
                  </Typography>
                  <Rating value={movie.rating / 2} precision={0.5} readOnly />
                  <Stack direction="row" spacing={1} sx={{ my: 1 }}>
                    {movie.genres.map((genre, i) => (
                      <Chip key={i} label={genre} size="small" />
                    ))}
                  </Stack>
                  <Typography variant="body2" color="text.secondary">
                    Runtime: {movie.runtime} minutes
                  </Typography>
                  <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                    {movie.tagline}
                  </Typography>
                </CardContent>
              </Card>
            </motion.div>
          </Grid>
        ))}
      </Grid>
    </Container>
  )
}

export default MovieRecommender 