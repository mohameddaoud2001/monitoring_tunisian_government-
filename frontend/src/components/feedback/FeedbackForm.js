import React, { useState } from 'react';
import { TextField, Button, Container, Typography, Box } from '@mui/material';
import api from '../../api';
import { useLanguage } from '../../contexts/LanguageContext';

function FeedbackForm({ projectId }) {
  const [content, setContent] = useState('');
  const [contentAr, setContentAr] = useState('');
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState('');
  const { language } = useLanguage();

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      const feedbackData = {
        project_id: projectId,
        content: language === 'en' ? content : '',
        content_ar: language === 'ar' ? contentAr : '',
      };
      await api.post('/feedback', feedbackData);
      setSuccess(true);
      setContent('');
      setContentAr('');
      setError('');
    } catch (err) {
      setError('Failed to submit feedback');
    }
  };

  return (
    <Container maxWidth="sm">
      <Box mt={5}>
        <Typography variant="h6">
          {language === 'en' ? 'Submit Feedback' : 'إرسال ملاحظات'}
        </Typography>
        {success && (
          <Typography color="primary">
            {language === 'en' ? 'Feedback submitted successfully!' : 'تم إرسال الملاحظات بنجاح!'}
          </Typography>
        )}
        {error && <Typography color="error">{error}</Typography>}
        <Box component="form" onSubmit={handleSubmit} mt={3}>
          {language === 'en' && (
            <TextField
              variant="outlined"
              margin="normal"
              required
              fullWidth
              multiline
              rows={4}
              label="Feedback (English)"
              value={content}
              onChange={(e) => setContent(e.target.value)}
            />
          )}
          {language === 'ar' && (
            <TextField
              variant="outlined"
              margin="normal"
              required
              fullWidth
              multiline
              rows={4}
              label="الملاحظات (عربي)"
              value={contentAr}
              onChange={(e) => setContentAr(e.target.value)}
            />
          )}
          <Button type="submit" variant="contained" color="primary" sx={{ mt: 2 }}>
            {language === 'en' ? 'Submit' : 'إرسال'}
          </Button>
        </Box>
      </Box>
    </Container>
  );
}

export default FeedbackForm;