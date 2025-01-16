# Use a lightweight Python image
FROM python:3.10-slim

# Set working directory in the container
WORKDIR /app

# Copy application files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Download TextBlob data
RUN python -m textblob.download_corpora

# Expose port for the Flask app
EXPOSE 5000

# Set Flask environment
ENV FLASK_ENV=development

# Command to run the app (using Gunicorn for production)
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "run:app"]