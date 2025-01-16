import React from 'react';
import { Typography, Box, Link } from '@mui/material';
import { useLanguage } from '../../contexts/LanguageContext';

function Footer() {
  const { language } = useLanguage();

  return (
    <Box component="footer" sx={{ bgcolor: 'background.paper', py: 6 }} mt={4}>
      <Container maxWidth="lg">
        <Typography variant="body2" color="text.secondary" align="center">
          {language === 'en'
            ? `Copyright © ${new Date().getFullYear()} Tunisian Government Project Monitoring.`
            : `حقوق النشر © ${new Date().getFullYear()} مراقبة المشاريع الحكومية التونسية.`}
          <br />
          {language === 'en' ? 'All rights reserved.' : 'كل الحقوق محفوظة.'}
          <br />
          <Link color="inherit" href="#">
            {language === 'en' ? 'Privacy Policy' : 'سياسة الخصوصية'}
          </Link>
          {' | '}
          <Link color="inherit" href="#">
            {language === 'en' ? 'Terms of Use' : 'شروط الاستخدام'}
          </Link>
        </Typography>
      </Container>
    </Box>
  );
}

export default Footer;