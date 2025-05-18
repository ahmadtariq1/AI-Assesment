import { ThemeProvider, createTheme, CssBaseline } from '@mui/material'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import MovieRecommender from './components/MovieRecommender'

const darkTheme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#e50914', // Netflix red
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

const queryClient = new QueryClient()

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider theme={darkTheme}>
        <CssBaseline />
        <MovieRecommender />
      </ThemeProvider>
    </QueryClientProvider>
  )
}

export default App
