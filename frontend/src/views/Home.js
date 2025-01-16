import React from 'react';
import { Container, Typography, Box } from '@mui/material';
import { useLanguage } from '../contexts/LanguageContext';

function Home() {
  const { language } = useLanguage();

  return (
    <Container maxWidth="md">
      <Box mt={5} textAlign="center">
        <Typography variant="h3" gutterBottom>
          {language === 'en' ? 'Welcome to the Tunisian Government Project Monitoring Platform' : 'مرحبًا بكم في منصة متابعة المشاريع الحكومية التونسية'}
        </Typography>
        <Typography variant="body1">
          {language === 'en' ? 'Explore ongoing projects, track progress, and provide feedback.' : 'استكشف المشاريع الجارية، تابع التقدم، وقدم الملاحظات.'}
        </Typography>
        {/* Add more content here, like an introduction, features, etc. */}
      </Box>
    </Container>
  );
}

export default Home;