import { useState } from 'react'
import {
  Box,
  Paper,
  Typography,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Radio,
  RadioGroup,
  FormControlLabel,
  TextField,
  Button,
  Card,
  CardContent,
  Chip,
  Stack,
  alpha,
} from '@mui/material'
import { Grid as MuiGrid } from '@mui/material'
import { motion } from 'framer-motion'
import axios from 'axios'

const Grid = MuiGrid as any

const genres = [
  'Action',
  'Adventure',
  'Animation',
  'Comedy',
  'Crime',
  'Documentary',
  'Drama',
  'Family',
  'Fantasy',
  'Horror',
  'Mystery',
  'Romance',
  'Sci-Fi',
  'Thriller',
]

interface MovieRecommenderProps {
  onRecommendations: (recs: any[]) => void
  recommendations: any[]
}

const API_URL = 'http://localhost:3001/api/recommend'

// Theme constants
const THEME = {
  background: '#121212',
  paper: '#1E1E1E',
  primary: '#3f51b5',
  text: '#FFFFFF',
  textSecondary: 'rgba(255, 255, 255, 0.7)',
  border: '1px solid rgba(255, 255, 255, 0.12)',
  error: '#f44336',
}

export const MovieRecommender = ({
  onRecommendations,
  recommendations,
}: MovieRecommenderProps) => {
  const [selectedGenres, setSelectedGenres] = useState<string[]>([])
  const [runtime, setRuntime] = useState('medium')
  const [age, setAge] = useState('25')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    
    const payload = {
      genres: selectedGenres,
      runtime,
      age: parseInt(age),
    }
    
    try {
      const response = await axios.post(API_URL, payload)
      if (response.data.success) {
        onRecommendations(response.data.recommendations)
      } else {
        setError(response.data.error || 'Failed to get recommendations')
      }
    } catch (error: any) {
      setError(error.message || 'Failed to connect to the recommendation service')
    } finally {
      setLoading(false)
    }
  }

  return (
    <Box sx={{ 
      maxWidth: 1200, 
      margin: '0 auto', 
      p: 3,
      color: THEME.text,
      bgcolor: THEME.background,
    }}>
      <Paper
        elevation={0}
        sx={{
          p: 4,
          mb: 4,
          background: THEME.paper,
          border: THEME.border,
          borderRadius: 2,
        }}
      >
        <Typography variant="h4" gutterBottom sx={{ 
          color: '#2C3E50',
          fontWeight: 600,
          mb: 4,
          textAlign: 'center',
          fontFamily: '"Inter", "Helvetica Neue", sans-serif',
          fontSize: '2.2rem',
        }}>
          Movie Recommendations
        </Typography>
        <form onSubmit={handleSubmit}>
          <Grid container spacing={4}>
            <Grid item xs={12} md={6}>
              <FormControl fullWidth>
                <InputLabel sx={{ color: THEME.textSecondary }}>Genre</InputLabel>
                <Select
                  multiple
                  value={selectedGenres}
                  onChange={(e) => setSelectedGenres(e.target.value as string[])}
                  label="Genre"
                  sx={{
                    '& .MuiOutlinedInput-notchedOutline': {
                      borderColor: 'rgba(255, 255, 255, 0.23)',
                    },
                    '&:hover .MuiOutlinedInput-notchedOutline': {
                      borderColor: THEME.primary,
                    },
                    '&.Mui-focused .MuiOutlinedInput-notchedOutline': {
                      borderColor: THEME.primary,
                    },
                    color: THEME.text
                  }}
                  renderValue={(selected) => (
                    <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                      {(selected as string[]).map((value) => (
                        <Chip 
                          key={value} 
                          label={value}
                          sx={{
                            backgroundColor: alpha(THEME.primary, 0.1),
                            color: THEME.text,
                            '&:hover': {
                              backgroundColor: alpha(THEME.primary, 0.2),
                            }
                          }}
                        />
                      ))}
                    </Box>
                  )}
                >
                  {genres.map((genre) => (
                    <MenuItem key={genre} value={genre}>
                      {genre}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} md={3}>
              <FormControl component="fieldset">
                <Typography variant="subtitle1" gutterBottom sx={{ color: THEME.text, mb: 2 }}>
                  Length
                </Typography>
                <RadioGroup
                  value={runtime}
                  onChange={(e) => setRuntime(e.target.value)}
                >
                  <FormControlLabel
                    value="short"
                    control={<Radio sx={{ color: THEME.textSecondary }} />}
                    label={<Typography sx={{ color: THEME.textSecondary }}>Short (under 90 min)</Typography>}
                  />
                  <FormControlLabel
                    value="medium"
                    control={<Radio sx={{ color: THEME.textSecondary }} />}
                    label={<Typography sx={{ color: THEME.textSecondary }}>Medium (90-150 min)</Typography>}
                  />
                  <FormControlLabel
                    value="long"
                    control={<Radio sx={{ color: THEME.textSecondary }} />}
                    label={<Typography sx={{ color: THEME.textSecondary }}>Long (over 150 min)</Typography>}
                  />
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
                InputProps={{ 
                  inputProps: { min: 0, max: 100 },
                  sx: { color: THEME.text }
                }}
                sx={{
                  '& .MuiOutlinedInput-notchedOutline': {
                    borderColor: 'rgba(255, 255, 255, 0.23)',
                  },
                  '&:hover .MuiOutlinedInput-notchedOutline': {
                    borderColor: THEME.primary,
                  },
                  '& .MuiInputLabel-root': {
                    color: THEME.textSecondary,
                  }
                }}
              />
            </Grid>
          </Grid>
          <Box sx={{ mt: 4, textAlign: 'center' }}>
            <Button
              variant="contained"
              type="submit"
              disabled={loading}
              sx={{
                px: 4,
                py: 1,
                bgcolor: THEME.primary,
                '&:hover': {
                  bgcolor: alpha(THEME.primary, 0.8),
                }
              }}
            >
              {loading ? 'Finding Movies...' : 'Get Recommendations'}
            </Button>
          </Box>
        </form>
      </Paper>

      {error && (
        <Paper
          elevation={0}
          sx={{ 
            p: 3,
            mb: 4,
            background: alpha(THEME.error, 0.1),
            border: `1px solid ${THEME.error}`,
            borderRadius: 2,
          }}
        >
          <Typography color={THEME.error}>{error}</Typography>
        </Paper>
      )}

      {recommendations.length > 0 && (
        <Grid container spacing={3}>
          {recommendations.map((movie, index) => (
            <Grid item xs={12} sm={6} md={4} key={index}>
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3, delay: index * 0.1 }}
              >
                <Card sx={{ 
                  height: '100%',
                  background: THEME.paper,
                  border: THEME.border,
                  borderRadius: 2,
                  transition: 'transform 0.2s ease-in-out',
                  '&:hover': {
                    transform: 'translateY(-4px)',
                  }
                }}>
                  <CardContent>
                    <Typography variant="h6" gutterBottom sx={{ 
                      color: THEME.text,
                      fontWeight: 500,
                      borderBottom: THEME.border,
                      pb: 1,
                    }}>
                      {movie.title}
                    </Typography>
                    <Box sx={{ mb: 2, display: 'flex', alignItems: 'center' }}>
                      <Typography variant="body2" sx={{ color: THEME.textSecondary, mr: 1 }}>
                        IMDB:
                      </Typography>
                      <Typography variant="h6" sx={{ 
                        color: THEME.primary,
                        fontWeight: 500,
                      }}>
                        {movie.rating.toFixed(1)}
                      </Typography>
                    </Box>
                    <Stack direction="row" spacing={1} sx={{ mb: 2, flexWrap: 'wrap', gap: 1 }}>
                      {movie.genres.map((genre: string) => (
                        <Chip
                          key={genre}
                          label={genre}
                          size="small"
                          sx={{
                            backgroundColor: alpha(THEME.primary, 0.1),
                            color: THEME.text,
                            '&:hover': {
                              backgroundColor: alpha(THEME.primary, 0.2),
                            }
                          }}
                        />
                      ))}
                    </Stack>
                    <Typography variant="body2" sx={{ 
                      color: THEME.textSecondary,
                      mb: 2,
                    }}>
                      {movie.description}
                    </Typography>
                    <Typography variant="body2" sx={{ 
                      color: THEME.textSecondary,
                      borderTop: THEME.border,
                      pt: 2,
                    }}>
                      Runtime: {movie.runtime} minutes
                    </Typography>
                  </CardContent>
                </Card>
              </motion.div>
            </Grid>
          ))}
        </Grid>
      )}
    </Box>
  )
} 