import React from 'react';
import { Drawer, List, ListItem, ListItemIcon, ListItemText, Divider } from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';
import DashboardIcon from '@mui/icons-material/Dashboard';
import ListAltIcon from '@mui/icons-material/ListAlt';
import RateReviewIcon from '@mui/icons-material/RateReview';
import { useLanguage } from '../../contexts/LanguageContext';

const drawerWidth = 240;

function Sidebar() {
  const { language } = useLanguage();

  const menuItems = [
    {
      text: language === 'en' ? 'Dashboard' : 'لوحة التحكم',
      icon: <DashboardIcon />,
      path: '/dashboard',
    },
    {
      text: language === 'en' ? 'Projects' : 'المشاريع',
      icon: <ListAltIcon />,
      path: '/projects',
    },
    {
      text: language === 'en' ? 'Feedback' : 'التعليقات',
      icon: <RateReviewIcon />,
      path: '/feedback',
    },
    // Add more menu items as needed
  ];

  return (
    <Drawer
      sx={{
        width: drawerWidth,
        flexShrink: 0,
        '& .MuiDrawer-paper': {
          width: drawerWidth,
          boxSizing: 'border-box',
        },
      }}
      variant="permanent" // or "temporary" for mobile responsiveness
      anchor="left"
    >
      <Toolbar />
      <Divider />
      <List>
        {menuItems.map((item) => (
          <ListItem button key={item.text} component={RouterLink} to={item.path}>
            <ListItemIcon>{item.icon}</ListItemIcon>
            <ListItemText primary={item.text} />
          </ListItem>
        ))}
      </List>
    </Drawer>
  );
}

export default Sidebar;