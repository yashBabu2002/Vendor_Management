# Use an official Python image as a base
FROM python:3.10

# Install system dependencies for GIS support
RUN apt-get update && apt-get install -y \
gdal-bin \
libgdal-dev \
libgeos-dev \
binutils \
libproj-dev \
libsqlite3-mod-spatialite \
&& apt-get clean

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
GDAL_LIBRARY_PATH=/usr/lib/x86_64-linux-gnu/libgdal.so \
GEOS_LIBRARY_PATH=/usr/lib/x86_64-linux-gnu/libgeos_c.so

# Set the working directory in the container
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project files
COPY . .

# Expose the application port
EXPOSE 8000

# Run migrations and start the Django server
CMD ["sh", "-c", "python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
