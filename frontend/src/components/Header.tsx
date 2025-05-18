import AppBar from '@mui/material/AppBar'
import Toolbar from '@mui/material/Toolbar'
import Typography from '@mui/material/Typography'
import MovieFilterIcon from '@mui/icons-material/MovieFilter'
import Box from '@mui/material/Box'

export const Header = () => {
  return (
    <AppBar position="static" color="transparent" elevation={0}>
      <Toolbar>
        <Box display="flex" alignItems="center" gap={2}>
          <MovieFilterIcon sx={{ fontSize: 40, color: 'primary.main' }} />
          <Typography
            variant="h5"
            component="div"
            sx={{
              flexGrow: 1,
              fontWeight: 'bold',
              background: 'linear-gradient(45deg, #e50914 30%, #ff8e53 90%)',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
            }}
          >
            Movie Recommender
          </Typography>
        </Box>
      </Toolbar>
    </AppBar>
  )
} 