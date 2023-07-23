import React from 'react'
import ReactDOM from 'react-dom/client'
import './index.css'
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";

import CollaborativeFilter from '../components/CollaborativeFilter/CollaborativeFilter'
import ContentFilter from '../components/ContentFilter/ContentFilter'
import AboutPage from '../components/AboutPage/AboutPage'
import NavBar from '../components/NavBar/NavBar'
import { createTheme, ThemeProvider } from '@mui/material/styles';
import {themeOptions} from '../themes/themeOptions'
const theme = createTheme(themeOptions);
const router = createBrowserRouter([
  {
    path: "/",
    element: <AboutPage/>,
  },
  {
    path:"/collaborativefilter",
    element: <CollaborativeFilter/>
  },
  {
    path:"/contentfilter",
    element: <ContentFilter/>
  },
  {
    path:"/about", 
    element:<AboutPage/>
  }
]);

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
        <ThemeProvider theme={theme}>
          <NavBar/>
          <RouterProvider router={router}/>
        </ThemeProvider>
  </React.StrictMode>,
)
