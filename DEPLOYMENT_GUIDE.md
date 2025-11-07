# RideShare Pro - Deployment Guide

## 📋 Pre-Deployment Checklist

- [ ] Code pushed to GitHub
- [ ] Environment variables configured
- [ ] Database backups created
- [ ] SSL certificates obtained
- [ ] Domain name configured
- [ ] CI/CD pipeline set up
- [ ] Monitoring tools configured
- [ ] Error tracking enabled

---

## 🚀 Deployment Options

### Option 1: Heroku Deployment (Recommended for Quick Start)

#### Backend Deployment
```bash
# Install Heroku CLI
curl https://cli.heroku.com/install.sh | sh

# Login to Heroku
heroku login

# Create Heroku app
heroku create rideshare-pro-api

# Add PostgreSQL addon
heroku addons:create heroku-postgresql:hobby-dev

# Set environment variables
heroku config:set DEBUG=False
heroku config:set SECRET_KEY=your-secret-key
heroku config:set ALLOWED_HOSTS=rideshare-pro-api.herokuapp.com

# Create Procfile
cat > Procfile << 'PROCEOF'
web: gunicorn rideshare_backend.wsgi:application --log-file -
release: python manage.py migrate
PROCEOF

# Deploy
git push heroku main

# Create superuser
heroku run python manage.py createsuperuser
```

#### Frontend Deployment
```bash
# Create Vercel account and install CLI
npm i -g vercel

# Deploy
vercel

# Set environment variables in Vercel dashboard
NEXT_PUBLIC_API_URL=https://rideshare-pro-api.herokuapp.com/api
```

---

### Option 2: AWS Deployment (Production)

#### Backend on EC2
```bash
# Launch EC2 instance (Ubuntu 20.04)
# SSH into instance
ssh -i your-key.pem ubuntu@your-instance-ip

# Install dependencies
sudo apt update
sudo apt install python3-pip python3-venv postgresql postgresql-contrib nginx

# Clone repository
git clone https://github.com/Aletien/Rideshare-Pro-.git
cd Rideshare-Pro-

# Setup Python environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure PostgreSQL
sudo -u postgres createdb rideshare_db
sudo -u postgres createuser rideshare_user
sudo -u postgres psql -c "ALTER USER rideshare_user WITH PASSWORD 'your-password';"

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Install Gunicorn
pip install gunicorn

# Create systemd service
sudo cat > /etc/systemd/system/rideshare.service << 'SERVICEEOF'
[Unit]
Description=RideShare Pro Django Application
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/Rideshare-Pro-
ExecStart=/home/ubuntu/Rideshare-Pro-/venv/bin/gunicorn \
    --workers 3 \
    --bind 127.0.0.1:8000 \
    rideshare_backend.wsgi:application

[Install]
WantedBy=multi-user.target
SERVICEEOF

# Start service
sudo systemctl start rideshare
sudo systemctl enable rideshare

# Configure Nginx
sudo cat > /etc/nginx/sites-available/rideshare << 'NGINXEOF'
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static/ {
        alias /home/ubuntu/Rideshare-Pro-/staticfiles/;
    }
}
NGINXEOF

# Enable Nginx site
sudo ln -s /etc/nginx/sites-available/rideshare /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# Setup SSL with Let's Encrypt
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

#### Frontend on S3 + CloudFront
```bash
# Build Next.js app
npm run build

# Create S3 bucket
aws s3 mb s3://rideshare-pro-frontend

# Upload build files
aws s3 sync out/ s3://rideshare-pro-frontend --delete

# Create CloudFront distribution
# Configure to point to S3 bucket
# Set custom domain
```

---

### Option 3: Docker Deployment

#### Create Dockerfile for Backend
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "rideshare_backend.wsgi:application", "--bind", "0.0.0.0:8000"]
```

#### Create Dockerfile for Frontend
```dockerfile
FROM node:18-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

FROM node:18-alpine

WORKDIR /app

COPY --from=builder /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package*.json ./

EXPOSE 3000

CMD ["npm", "start"]
```

#### Docker Compose
```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: rideshare_db
      POSTGRES_USER: rideshare_user
      POSTGRES_PASSWORD: your-password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  backend:
    build: .
    command: >
      sh -c "python manage.py migrate &&
             gunicorn rideshare_backend.wsgi:application --bind 0.0.0.0:8000"
    ports:
      - "8000:8000"
    environment:
      DEBUG: "False"
      SECRET_KEY: your-secret-key
      DATABASE_URL: postgresql://rideshare_user:your-password@db:5432/rideshare_db
    depends_on:
      - db

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      NEXT_PUBLIC_API_URL: http://backend:8000/api

volumes:
  postgres_data:
```

---

## 🔧 Environment Configuration

### Backend (.env)
```
DEBUG=False
SECRET_KEY=your-very-secret-key-here
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://user:password@localhost:5432/rideshare_db
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
STRIPE_PUBLIC_KEY=pk_live_...
STRIPE_SECRET_KEY=sk_live_...
```

### Frontend (.env.production)
```
NEXT_PUBLIC_API_URL=https://api.yourdomain.com/api
NEXT_PUBLIC_APP_NAME=RideShare Pro
```

---

## 📊 Monitoring & Logging

### Backend Monitoring
```bash
# Install monitoring tools
pip install django-extensions django-debug-toolbar

# Setup error tracking
pip install sentry-sdk

# Configure Sentry in settings.py
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,
)
```

### Frontend Monitoring
```bash
# Install Sentry for Next.js
npm install @sentry/nextjs

# Configure in next.config.js
const withSentry = require("@sentry/nextjs").withSentry;

module.exports = withSentry({
  sentry: {
    dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  },
});
```

---

## 🔐 Security Hardening

### Backend Security
```python
# settings.py

# HTTPS
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Security headers
SECURE_CONTENT_SECURITY_POLICY = {
    "default-src": ("'self'",),
    "script-src": ("'self'", "'unsafe-inline'"),
    "style-src": ("'self'", "'unsafe-inline'"),
}

# Rate limiting
RATELIMIT_ENABLE = True
RATELIMIT_USE_CACHE = "default"
```

### Frontend Security
```javascript
// next.config.js

const securityHeaders = [
  {
    key: 'X-Content-Type-Options',
    value: 'nosniff'
  },
  {
    key: 'X-Frame-Options',
    value: 'DENY'
  },
  {
    key: 'X-XSS-Protection',
    value: '1; mode=block'
  }
];

module.exports = {
  async headers() {
    return [
      {
        source: '/:path*',
        headers: securityHeaders,
      },
    ];
  },
};
```

---

## 📈 Performance Optimization

### Backend
```bash
# Enable caching
pip install django-redis

# Configure in settings.py
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
    }
}

# Database optimization
# Add indexes to frequently queried fields
# Use select_related() and prefetch_related()
# Implement pagination
```

### Frontend
```bash
# Image optimization
npm install next-image-export-optimizer

# Code splitting
# Dynamic imports for large components
import dynamic from 'next/dynamic';

const HeavyComponent = dynamic(() => import('./HeavyComponent'), {
  loading: () => <p>Loading...</p>,
});
```

---

## 🔄 CI/CD Pipeline (GitHub Actions)

```yaml
# .github/workflows/deploy.yml

name: Deploy

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.11
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      - name: Run tests
        run: |
          python manage.py test

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Heroku
        uses: akhileshns/heroku-deploy@v3.12.12
        with:
          heroku_api_key: ${{ secrets.HEROKU_API_KEY }}
          heroku_app_name: "rideshare-pro-api"
          heroku_email: ${{ secrets.HEROKU_EMAIL }}
```

---

## 📝 Post-Deployment Checklist

- [ ] Verify backend API is responding
- [ ] Verify frontend is loading
- [ ] Test user registration
- [ ] Test user login
- [ ] Test ride request flow
- [ ] Verify database backups
- [ ] Monitor error logs
- [ ] Check performance metrics
- [ ] Test payment processing
- [ ] Verify email notifications

---

## 🆘 Troubleshooting

### Backend Issues
```bash
# Check logs
tail -f /var/log/rideshare/django.log

# Restart service
sudo systemctl restart rideshare

# Check database connection
python manage.py dbshell

# Run migrations
python manage.py migrate
```

### Frontend Issues
```bash
# Check build
npm run build

# Check logs
npm run dev

# Clear cache
rm -rf .next
npm run build
```

---

## 📞 Support

For deployment issues:
1. Check logs carefully
2. Review environment variables
3. Verify database connectivity
4. Check firewall rules
5. Contact support team

---

**Last Updated:** November 7, 2025
**Version:** 1.0.0

