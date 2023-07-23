import { AppBar, Toolbar, Typography, Button } from '@mui/material';

const Navbar = () => {
  return (
    <AppBar position="static" color="primary">
      <Toolbar>
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          My Website
        </Typography>
        <Button color="inherit" href='/about' >About</Button>
        <Button color="inherit" href='/contentfilter' >Content-Based Filter</Button>
        <Button color="inherit" href='/collaborativefilter' >Collaborative Filter</Button>
      </Toolbar>
    </AppBar>
  );
};

export default Navbar;