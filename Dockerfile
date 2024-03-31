FROM python:3.11-slim


# Install build dependencies and curl
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libssl-dev \
    libpcre3-dev \
    curl \
    nginx \
    supervisor \
    && rm -rf /var/lib/apt/lists/*


RUN pip install gunicorn==21.2.0

# Configure Nginx
RUN rm /etc/nginx/sites-enabled/default
COPY nginx.conf /etc/nginx/sites-available/
RUN ln -s /etc/nginx/sites-available/nginx.conf /etc/nginx/sites-enabled/

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Copy requirements file and install dependencies
COPY requirement.txt requirement.txt
RUN pip install --no-cache-dir -r requirement.txt

# Copy the rest of the project files
COPY . .

RUN python manage.py migrate

# Recopilar archivos estáticos
RUN python manage.py collectstatic --no-input

# COPY /staticfiles /usr/share/nginx/html/staticfiles

# Expose the server port
EXPOSE 80


# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "configs.wsgi:application"]
CMD ["/usr/bin/supervisord"]
