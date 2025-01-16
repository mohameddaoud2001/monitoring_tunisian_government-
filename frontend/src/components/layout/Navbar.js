import React from 'react';
import { AppBar, Toolbar, Typography, Button } from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';
import { useLanguage } from '../../contexts/LanguageContext';

function Navbar() {
    const { language, toggleLanguage } = useLanguage();

    return (
        <AppBar position="static">
            <Toolbar>
                <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
                    <RouterLink to="/" style={{ textDecoration: 'none', color: 'inherit' }}>
                        {language === 'en' ? 'Tunisian Projects' : 'المشاريع التونسية'}
                    </RouterLink>
                </Typography>
                <Button color="inherit" component={RouterLink} to="/projects">
                    {language === 'en' ? 'Projects' : 'المشاريع'}
                </Button>
                <Button color="inherit" component={RouterLink} to="/login">
                    {language === 'en' ? 'Login' : 'تسجيل الدخول'}
                </Button>
                <Button color="inherit" component={RouterLink} to="/register">
                    {language === 'en' ? 'Register' : 'تسجيل'}
                </Button>
                <Button color="inherit" onClick={toggleLanguage}>
                    {language === 'en' ? 'عربي' : 'English'}
                </Button>
            </Toolbar>
        </AppBar>
    );
}

export default Navbar;