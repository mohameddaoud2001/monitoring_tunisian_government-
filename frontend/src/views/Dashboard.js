import React from 'react';
import { Container, Typography } from '@mui/material';
import { useLanguage } from '../contexts/LanguageContext';

function Dashboard() {
  const { language } = useLanguage();

  return (
    <Container>
      <Typography variant="h4" gutterBottom>
        {language === 'en' ? 'Dashboard' : 'لوحة التحكم'}
      </Typography>
      {/* Add user-specific content here, like projects they're involved in, etc. */}
    </Container>
  );
}

export default Dashboard;