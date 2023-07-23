import { useEffect, useState } from "react";
import axios from 'axios'
import { Box, Stack } from "@mui/system";
import { List, ListItem, ListItemButton, ListItemText, TextField, Typography } from "@mui/material";
import Fuse from 'fuse.js'

interface IMovieResponse{
    
        imdbId: number,
        movieId: number,
        title: string,
        users: [number],
        year: number
    
}

interface IRecommendationRespone{
    
        genres: string,
        movieid: number,
        title: string,
        year: number
    
}

const ContentFilter = () => {
    const [movies, setMovies] = useState<IMovieResponse[]>([]);
    const [searchResults , setSearchResults] = useState<IMovieResponse[]>([]);
    const [reccomendationsToShow, setReccomendationsToShow] = useState<IRecommendationRespone[]>([])
    useEffect(() => {
      // Function to fetch movies data from the API
      const fetchMovies = async () => {
        try {
          const response = await axios.get('http://localhost:5000/api/movies');
          setMovies(response.data); // Assuming the response contains the movie data as an array
        } catch (error) {
          console.error('Error fetching movies:', error);
        }
      };
  
      fetchMovies();
    }, []);
    const fuseOptions = {
        keys: [
            "title",
        ]
    };

    const fuse = new Fuse(movies, fuseOptions)
    
    const showReccomendations = async (movie: string) => {
        const requestBody = {
            movie_title: movie,
            top_recommendations: 10,
        };
        try {
            const response = await axios.post('http://localhost:5000/api/cbr', requestBody);
            console.log('Post request successful. Response:', response.data);
            const data: IRecommendationRespone[] = response.data
            setReccomendationsToShow(data)
          } catch (error) {
            console.error('Error posting data:', error);
          }
        
    }

    return (
        <Stack sx={{backgroundColor:"gray", height:"100vh", width:"100vw"}}
        direction="row"
        justifyContent="space-around"
        alignItems="center"
        spacing={1}
        >
            <Stack
            sx={{marginTop:"10em"}}
            direction="row"
            justifyContent="center"
            alignItems="center"
            spacing={2}
            >
                <Stack>
                <TextField id="outlined-basic" label="Outlined" variant="outlined" onChange={(e)=>{
                    setSearchResults(fuse.search(e.target.value).map(({item})=>item))
                    console.log(fuse.search(e.target.value))
                }} />
                <Box>
                    <List>
                        {searchResults.slice(0, 10).map((item)=>{
                        return (
                        <ListItem disablePadding>
                            <ListItemButton onClick={()=>{showReccomendations(item.title)}}>
                                <ListItemText primary={item.title} />
                            </ListItemButton>
                        </ListItem>
                        )
                        })}
                    </List>
                </Box>
                </Stack>
                <Stack>
                    <Typography>Twoje 10 rekomendacji to:</Typography>
                    {reccomendationsToShow.map((item)=>{
                        return (
                            <div>{item.title}</div>
                        )
                    })}
                </Stack>   
            </Stack>
        <Stack/>
    </Stack>
    );
};

export default ContentFilter;