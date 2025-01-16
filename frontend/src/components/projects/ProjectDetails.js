import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { Container, Typography, Box, CircularProgress } from '@mui/material';
import api from '../../api';
import { useLanguage } from '../../contexts/LanguageContext';

function ProjectDetails() {
  const { projectId } = useParams();
  const [project, setProject] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const { language } = useLanguage();

  useEffect(() => {
    const fetchProject = async () => {
      try {
        const response = await api.get(`/projects/${projectId}`);
        setProject(response.data);
      } catch (err) {
        setError('Failed to load project details');
      } finally {
        setLoading(false);
      }
    };

    fetchProject();
  }, [projectId]);

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return <Typography color="error">{error}</Typography>;
  }

  return (
    <Container>
      <Box mt={4}>
        <Typography variant="h4">
          {language === 'en' ? project.title : project.title_ar}
        </Typography>
        <Typography variant="body1">
          {language === 'en' ? project.description : project.description_ar}
        </Typography>
        <Typography variant="body2">
          {language === 'en' ? 'Status:' : 'الحالة:'} {project.status}
        </Typography>
        {/* Add more details like budget, deliverables, etc. */}
      </Box>
    </Container>
  );
}

export default ProjectDetails;