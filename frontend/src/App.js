import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { useLanguage } from './contexts/LanguageContext';
import RTL from './RTL'; // Import RTL component
import Navbar from './components/layout/Navbar';
import Home from './views/Home';
import Projects from './views/Projects';
import Login from './views/Login';
import Register from './views/Register';
import Dashboard from './views/Dashboard';

const ltrTheme = createTheme({
    direction: 'ltr',
    palette: {
        primary: {
            main: '#00796b',
        },
        secondary: {
            main: '#ffc107',
        },
    },
});

const rtlTheme = createTheme({
    direction: 'rtl',
    palette: {
        primary: {
            main: '#00796b',
        },
        secondary: {
            main: '#ffc107',
        },
    },
});

function App() {
    const { language } = useLanguage();

    return (
        <ThemeProvider theme={language === 'ar' ? rtlTheme : ltrTheme}>
            <RTL>
                <Router>
                    <Navbar />
                    <Routes>
                        <Route path="/" element={<Home />} />
                        <Route path="/projects" element={<Projects />} />
                        <Route path="/login" element={<Login />} />
                        <Route path="/register" element={<Register />} />
                        <Route path="/dashboard" element={<Dashboard />} />
                    </Routes>
                </Router>
            </RTL>
        </ThemeProvider>
    );
}

export default App;