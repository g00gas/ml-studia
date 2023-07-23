import { useEffect, useState } from "react";
import axios from "axios";
import { Box, Grid, Stack } from "@mui/material";
import { List, ListItem, ListItemButton, ListItemText, TextField, Typography } from "@mui/material";
import Fuse from "fuse.js";
import { useTheme } from "@mui/material/styles";

interface IMovieResponse {
  imdbId: number;
  movieId: number;
  title: string;
  users: [number];
  year: number;
}

interface IRecommendationRespone {
  genres: string;
  movieid: number;
  title: string;
  year: number;
}

const ContentFilter = () => {
  const theme = useTheme();

  const [movies, setMovies] = useState<IMovieResponse[]>([]);
  const [searchResults, setSearchResults] = useState<IMovieResponse[]>([]);
  const [recommendationsToShow, setRecommendationsToShow] = useState<IRecommendationRespone[]>([]);

  useEffect(() => {
    const fetchMovies = async () => {
      try {
        const response = await axios.get("http://localhost:5000/api/movies");
        setMovies(response.data);
      } catch (error) {
        console.error("Error fetching movies:", error);
      }
    };

    fetchMovies();
  }, []);

  const fuseOptions = {
    keys: ["title"],
  };

  const fuse = new Fuse(movies, fuseOptions);

  const showRecommendations = async (movie: string) => {
    const requestBody = {
      movie_title: movie,
      top_recommendations: 10,
    };
    try {
      const response = await axios.post("http://localhost:5000/api/cbr", requestBody);
      console.log("Post request successful. Response:", response.data);
      const data: IRecommendationRespone[] = response.data;
      setRecommendationsToShow(data);
    } catch (error) {
      console.error("Error posting data:", error);
    }
  };

  return (
    <Stack
      sx={{
        backgroundColor: theme.palette.background.default,
        minHeight: "100vh",
        width: "100vw",
      }}
      direction="row"
      justifyContent="center"
      alignItems="center"
      spacing={4}
    >
      <Stack spacing={2} maxWidth={400}>
        <Typography variant="h4" sx={{ textAlign: "center", color: theme.palette.primary.main }}>
          Wyszukaj Film
        </Typography>
        <TextField
          id="outlined-basic"
          label="Wpisz tytuł"
          variant="outlined"
          onChange={(e) => {
            setSearchResults(fuse.search(e.target.value).map(({ item }) => item));
          }}
        />
        <List>
          {searchResults.slice(0, 10).map((item) => (
            <ListItem key={item.imdbId} disablePadding>
              <ListItemButton onClick={() => showRecommendations(item.title)}>
                <ListItemText primary={item.title} />
              </ListItemButton>
            </ListItem>
          ))}
        </List>
      </Stack>
      <Stack spacing={2} maxWidth={600}>
        <Typography variant="h5" sx={{ color: theme.palette.secondary.main }}>
          Top 10 rekoendacji:
        </Typography>
        <Grid container spacing={2}>
          {recommendationsToShow.map((item) => (
            <Grid item xs={12} sm={6} md={4} key={item.movieid}>
              <Box
                sx={{
                  border: "1px solid",
                  borderColor: theme.palette.text.secondary,
                  borderRadius: theme.shape.borderRadius,
                  padding: 2,
                  backgroundColor: theme.palette.background.paper,
                }}
              >
                <Typography variant="subtitle1">{item.title}</Typography>
                <Typography variant="body2">Rodzaj: {item.genres.split('|').map((genreItem)=>{return `${genreItem}, `})}</Typography>
                <Typography variant="body2">Rok produkcji: {item.year}</Typography>
              </Box>
            </Grid>
          ))}
        </Grid>
      </Stack>
    </Stack>
  );
};

export default ContentFilter;
