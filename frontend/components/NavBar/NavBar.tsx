import { AppBar, Toolbar, Typography, Button } from '@mui/material';

const Navbar = () => {
  return (
    <AppBar position="static" color="primary">
      <Toolbar>
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          Projekt Machine Learning
        </Typography>
        <Button color="inherit" href='/about' >O nas</Button>
        <Button color="inherit" href='/contentfilter' >Filtr na zawartości</Button>
        <Button color="inherit" href='/collaborativefilter' >Filtr Kolaboratywny</Button>
      </Toolbar>
    </AppBar>
  );
};

export default Navbar;