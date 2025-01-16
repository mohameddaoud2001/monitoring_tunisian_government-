import React, { useState, useEffect } from 'react';
import { Container, Typography, Grid, CircularProgress } from '@mui/material';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import api from '../../api';
import { useLanguage } from '../../contexts/LanguageContext';

function StatsDashboard() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const { language } = useLanguage();

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const response = await api.get('/stats/projects');
        setStats(response.data);
      } catch (error) {
        console.error('Error fetching stats:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchStats();
  }, []);

  if (loading) {
    return (
      <Container>
        <CircularProgress />
      </Container>
    );
  }

  if (!stats) {
    return (
      <Container>
        <Typography>
          {language === 'en' ? 'No stats available.' : 'لا توجد إحصائيات متاحة.'}
        </Typography>
      </Container>
    );
  }

  const projectsByRegionData = stats.projects_by_region.map((item) => ({
    name: language === 'en' ? item.region_name : item.region_name_ar,
    count: item.project_count,
  }));

  const projectsByMinistryData = stats.projects_by_ministry.map((item) => ({
    name: language === 'en' ? item.ministry_name : item.ministry_name_ar,
    count: item.project_count,
  }));

  return (
    <Container>
      <Typography variant="h4" gutterBottom>
        {language === 'en' ? 'Project Statistics' : 'إحصائيات المشروع'}
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Typography variant="h6">
            {language === 'en' ? 'Projects by Region' : 'المشاريع حسب المنطقة'}
          </Typography>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={projectsByRegionData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="count" fill="#8884d8" />
            </BarChart>
          </ResponsiveContainer>
        </Grid>

        <Grid item xs={12} md={6}>
          <Typography variant="h6">
            {language === 'en' ? 'Projects by Ministry' : 'المشاريع حسب الوزارة'}
          </Typography>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={projectsByMinistryData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="count" fill="#82ca9d" />
            </BarChart>
          </ResponsiveContainer>
        </Grid>

        {/* Add more charts for other statistics as needed */}
      </Grid>
    </Container>
  );
}

export default StatsDashboard;