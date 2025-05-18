import { useState } from 'react'
import { ThemeProvider, createTheme } from '@mui/material/styles'
import CssBaseline from '@mui/material/CssBaseline'
import Container from '@mui/material/Container'
import Box from '@mui/material/Box'
import { MovieRecommender } from './components/MovieRecommender'
import { Header } from './components/Header'

const darkTheme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#e50914', // Netflix-like red
    },
    secondary: {
      main: '#ffffff',
    },
    background: {
      default: '#141414',
      paper: '#1f1f1f',
    },
  },
  typography: {
    fontFamily: [
      '-apple-system',
      'BlinkMacSystemFont',
      '"Segoe UI"',
      'Roboto',
      '"Helvetica Neue"',
      'Arial',
      'sans-serif',
    ].join(','),
  },
})

function App() {
  const [recommendations, setRecommendations] = useState([])

  return (
    <ThemeProvider theme={darkTheme}>
      <CssBaseline />
      <Box
        sx={{
          minHeight: '100vh',
          background: 'linear-gradient(to bottom, #000000, #141414)',
        }}
      >
        <Header />
        <Container maxWidth="lg" sx={{ pt: 4, pb: 8 }}>
          <MovieRecommender
            onRecommendations={setRecommendations}
            recommendations={recommendations}
          />
        </Container>
      </Box>
    </ThemeProvider>
  )
}

export default App
