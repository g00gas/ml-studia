import { useTheme } from "@mui/material/styles";
import { Box } from '@mui/system';
import { Typography } from '@mui/material';

const About = () => {
    const theme = useTheme();
  return (
    <Box
    sx={{
      backgroundColor: theme.palette.background.default,
      minHeight: '100vh',
      padding: '2rem',
    }}
  >
    <Typography variant="h4" sx={{ textAlign: 'center', color: theme.palette.primary.main, marginBottom: '2rem' }}>
      Strona O Nas
    </Typography>
    <Typography variant="h3" sx={{ textAlign: 'center', color: theme.palette.primary.main, marginBottom: '2rem' }}>
      Kto:
    </Typography>
    <Typography variant="h6" sx={{ textAlign: 'center', color: theme.palette.primary.main, marginBottom: '2rem' }}>
      Michał Gugała, numer albumu: 145550, adres email: <a href="mailto:pzx113965@student.wsb.poznan.pl">pzx113965@student.wsb.poznan.pl</a>
    </Typography>
    <Typography variant="h6" sx={{ textAlign: 'center', color: theme.palette.primary.main, marginBottom: '2rem' }}>
    Kacper Banasiak, numer albumu: 139688, adres email: <a href="mailto:pzx111404@student.wsb.poznan.pl">pzx111404@student.wsb.poznan.pl</a>
    </Typography>
    <Typography variant="h3" sx={{ textAlign: 'center', color: theme.palette.primary.main, marginBottom: '2rem' }}>
      Stack:
    </Typography>
    <Typography variant="h6" sx={{ textAlign: 'center', color: theme.palette.primary.main, marginBottom: '2rem' }}>
        Frontend: React + Vite
    </Typography>
    <Typography variant="h6" sx={{ textAlign: 'center', color: theme.palette.primary.main, marginBottom: '2rem' }}>
        Backend: Flask + PostgresSQL
    </Typography>
    <Typography variant="h6" sx={{ textAlign: 'center', color: theme.palette.primary.main, marginBottom: '2rem' }}>
        Infrastruktura: Docker
    </Typography>
    <Typography variant="h6" sx={{ textAlign: 'center', color: theme.palette.primary.main, marginBottom: '2rem' }}>
        Machine Learning: sklearn
    </Typography>
  </Box>
  );
};

export default About;