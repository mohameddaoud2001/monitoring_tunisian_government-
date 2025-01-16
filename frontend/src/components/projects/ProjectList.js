import React, { useState, useEffect } from "react";
import {
  Grid,
  Card,
  CardContent,
  Typography,
  CircularProgress,
  Box,
} from "@mui/material";
import api from "../../api";
import { useLanguage } from "../../contexts/LanguageContext";

function ProjectList() {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const { language } = useLanguage();

  useEffect(() => {
    const fetchProjects = async () => {
      try {
        const response = await api.get("/projects");
        console.log("API Response:", response); // Log the entire response

        // Check if the response is what you expect
        if (response.status === 200 && response.data && response.data.data) {
          setProjects(response.data.data);
        } else {
          console.error("Unexpected response format:", response);
          setProjects([]); // Set to empty or handle appropriately
        }
      } catch (error) {
        console.error("Error fetching projects:", error);
        if (error.response) {
            console.error("Response data:", error.response.data);
            console.error("Response status:", error.response.status);
            console.error("Response headers:", error.response.headers);
        } else if (error.request) {
            console.error("No response received:", error.request);
        }
      } finally {
        setLoading(false);
      }
    };

    fetchProjects();
  }, []);

  if (loading) {
    return (
      <Box
        display="flex"
        justifyContent="center"
        alignItems="center"
        minHeight="100vh"
      >
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Grid container spacing={2} style={{ padding: 20 }}>
      {projects.map((project) => (
        <Grid item xs={12} sm={6} md={4} key={project.id}>
          <Card>
            <CardContent>
              <Typography variant="h5" component="div">
                {language === "en" ? project.title : project.title_ar}
              </Typography>
              <Typography variant="body2">
                {language === "en"
                  ? project.description
                  : project.description_ar}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      ))}
    </Grid>
  );
}

export default ProjectList;