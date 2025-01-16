import React from 'react';
import { Card, CardContent, Typography, Button, CardActions } from '@mui/material';
import { useLanguage } from '../../contexts/LanguageContext';

function ProjectCard({ project, onProjectSelect }) {
  const { language } = useLanguage();

  return (
    <Card sx={{ minWidth: 275, mb: 2 }}>
      <CardContent>
        <Typography variant="h5" component="div">
          {language === 'en' ? project.title : project.title_ar}
        </Typography>
        <Typography color="text.secondary" gutterBottom>
          {language === 'en'
            ? `Status: ${project.status}`
            : `الحالة: ${project.status}`}
        </Typography>
        <Typography variant="body2">
          {language === 'en'
            ? project.description
            : project.description_ar}
        </Typography>
      </CardContent>
      <CardActions>
        <Button size="small" onClick={() => onProjectSelect(project)}>
          {language === 'en' ? 'Learn More' : 'لمعرفة المزيد'}
        </Button>
      </CardActions>
    </Card>
  );
}

export default ProjectCard;