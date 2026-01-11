# 🚀 PDD Generator - Production Deployment Guide

This guide covers everything you need to deploy the PDD Generator to production.

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Configuration](#configuration)
3. [Local Development Setup](#local-development)
4. [Docker Deployment](#docker-deployment)
5. [Cloud Deployment Options](#cloud-deployment)
6. [Environment Variables](#environment-variables)
7. [Security Considerations](#security)
8. [Monitoring & Maintenance](#monitoring)
9. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Software
- **Python**: 3.11 or higher
- **Node.js**: 18 or higher
- **Docker**: 20.10 or higher (for containerized deployment)
- **Git**: For cloning the repository

### Required Accounts
- **OpenAI API Account**: For LLM and Whisper access
- Optional: **GitHub**, **GitLab**, or other Git hosting

---

## Configuration

### Configuration Priority

The application uses a hierarchical configuration system:

1. **Environment Variables** (highest priority) - Override everything
2. **config.yaml** - Default configuration file
3. **Code Defaults** (lowest priority) - Fallback values

### Quick Setup

1. **Copy environment template**:
   ```bash
   cd backend
   cp .env.example .env
   ```

2. **Edit `.env` file** with your values:
   ```bash
   # Required
   OPENAI_API_KEY=sk-your-actual-key-here

   # Optional (with defaults shown)
   OPENAI_MODEL=gpt-4o
   OPENAI_TEMPERATURE=0.0
   APP_ENV=production
   ```

3. **Review `config.yaml`** for additional settings:
   ```bash
   cd backend
   nano config.yaml  # or your preferred editor
   ```

---

## Local Development Setup

### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Create virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your OpenAI API key
   ```

5. **Run the server**:
   ```bash
   uvicorn main:app --reload --port 8000
   ```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Create environment file**:
   ```bash
   # Create .env file with API URL
   echo "VITE_API_URL=http://localhost:8000" > .env
   ```

4. **Run the development server**:
   ```bash
   npm run dev
   ```

The frontend will be available at `http://localhost:3000` (or port 5173 for Vite)

---

## Docker Deployment

### Quick Start with Docker Compose

1. **Ensure Docker is installed**:
   ```bash
   docker --version
   docker-compose version
   ```

2. **Clone the repository**:
   ```bash
   git clone https://github.com/siddu509/AutoPDDGeneration.git
   cd AutoPDDGeneration
   ```

3. **Set up environment**:
   ```bash
   cp backend/.env.example backend/.env
   # Edit backend/.env with your OpenAI API key
   nano backend/.env
   ```

4. **Start all services**:
   ```bash
   docker-compose up -d
   ```

5. **Access the application**:
   - Frontend: `http://localhost:3000`
   - Backend API: `http://localhost:8000`
   - API Docs: `http://localhost:8000/docs`

6. **View logs**:
   ```bash
   docker-compose logs -f backend
   docker-compose logs -f frontend
   ```

7. **Stop services**:
   ```bash
   docker-compose down
   ```

### Building Docker Images Manually

#### Backend Image
```bash
cd backend
docker build -t pdd-generator-backend:latest .
docker run -p 8000:8000 \
  -e OPENAI_API_KEY=your-key-here \
  pdd-generator-backend:latest
```

#### Frontend Image
```bash
cd frontend
docker build -t pdd-generator-frontend:latest .
docker run -p 3000:80 \
  -e VITE_API_URL=http://your-backend-url:8000 \
  pdd-generator-frontend:latest
```

---

## Cloud Deployment Options

### Option 1: Render (Recommended for Easy Deployment)

#### Backend Deployment
1. Create a new **Web Service** on Render
2. Connect your GitHub repository
3. Configure:
   - **Build Command**: `cd backend && pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Environment Variables**:
     - `OPENAI_API_KEY`: Your OpenAI API key
     - `OPENAI_MODEL`: `gpt-4o` (or your preferred model)
     - `APP_ENV`: `production`

#### Frontend Deployment
1. Create a new **Static Site** on Render
2. Connect your GitHub repository
3. Configure:
   - **Build Command**: `cd frontend && npm run build`
   - **Publish Directory**: `frontend/dist`
   - **Environment Variables**:
     - `VITE_API_URL`: Your backend Render URL

### Option 2: AWS (Elastic Beanstalk)

1. **Backend (Elastic Beanstalk)**:
   ```bash
   # Install AWS EB CLI
   pip install awsebcli

   # Initialize
   cd backend
   eb init -p python-3.11
   eb create production-environment
   ```

2. **Frontend (S3 + CloudFront)**:
   ```bash
   # Build frontend
   cd frontend
   npm run build

   # Deploy to S3
   aws s3 sync dist s3://your-bucket-name --delete
   ```

### Option 3: DigitalOcean App Platform

1. **Create an app** in DigitalOcean Control Panel
2. **Select your repository**
3. **Configure**:
   - **Run Command**: `uvicorn main:app --host 0.0.0.0 --port 8000`
   - **HTTP Port**: `8000`
   - **Environment Variables**: Add your OpenAI API key

### Option 4: Google Cloud Run

#### Backend
```bash
# Build and push image
gcloud builds submit --tag gcr.io/PROJECT_ID/backend

# Deploy
gcloud run deploy backend \
  --image gcr.io/PROJECT_ID/backend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars OPENAI_API_KEY=your-key,OPENAI_MODEL=gpt-4o
```

#### Frontend
```bash
# Build and deploy
npm run build
gcloud app deploy frontend --project=PROJECT_ID
```

### Option 5: Kubernetes (for large-scale deployment)

See `k8s/` directory (to be created) for Kubernetes manifests.

---

## Environment Variables

### Required Variables

| Variable | Description | Example | Default |
|----------|-------------|---------|---------|
| `OPENAI_API_KEY` | OpenAI API key | `sk-proj-...` | None (required) |

### Optional Variables

#### Application Settings
| Variable | Description | Options | Default |
|----------|-------------|---------|---------|
| `APP_ENV` | Environment | `development`, `staging`, `production` | `production` |
| `APP_DEBUG` | Debug mode | `true`, `false` | `false` |
| `APP_LOG_LEVEL` | Logging level | `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL` | `INFO` |

#### LLM Settings
| Variable | Description | Options | Default |
|----------|-------------|---------|---------|
| `OPENAI_MODEL` | LLM model for PDD generation | `gpt-4o`, `gpt-4-turbo`, `gpt-3.5-turbo` | `gpt-4o` |
| `OPENAI_TEMPERATURE` | LLM temperature (0.0-1.0) | `0.0` (deterministic) to `1.0` (creative) | `0.0` |
| `WHISPER_MODEL` | Whisper model for transcription | `whisper-1` | `whisper-1` |
| `OPENAI_API_BASE` | OpenAI API base URL | Any valid OpenAI endpoint | `https://api.openai.com/v1` |

#### Server Settings
| Variable | Description | Default |
|----------|-------------|---------|
| `SERVER_HOST` | Server bind address | `0.0.0.0` |
| `SERVER_PORT` | Server port | `8000` |
| `SERVER_WORKERS` | Number of worker processes | `4` |

#### Rate Limiting
| Variable | Description | Default |
|----------|-------------|---------|
| `RATE_LIMIT_ENABLED` | Enable rate limiting | `true` |
| `RATE_LIMIT_PDD_GENERATION` | PDD generation limit | `10/minute` |
| `RATE_LIMIT_FILE_UPLOAD` | File upload limit | `5/minute` |
| `RATE_LIMIT_REFINE` | Section refinement limit | `20/minute` |
| `RATE_LIMIT_CHAT` | Chat endpoint limit | `30/minute` |

#### CORS
| Variable | Description | Example |
|----------|-------------|---------|
| `CORS_ORIGINS` | Allowed origins (comma-separated) | `http://localhost:3000,https://yourdomain.com` |

#### File Processing
| Variable | Description | Default |
|----------|-------------|---------|
| `MAX_FILE_SIZE_MB` | Maximum upload file size | `100` |
| `TEMP_DIR` | Temporary file directory | `/tmp` |

---

## Security Considerations

### 1. API Key Management

**Never commit your `.env` file** to version control!

- ✅ `.env.example` is committed (template only)
- ❌ `.env` is in `.gitignore` (never commit)

### 2. Production Checklist

- [ ] Change all default passwords
- [ ] Set `APP_ENV=production`
- [ ] Set `APP_DEBUG=false`
- [ ] Use HTTPS in production
- [ ] Configure CORS for your domain only
- [ ] Enable rate limiting
- [ ] Set up monitoring
- [ ] Configure backup strategy
- [ ] Review and update security headers
- [ ] Test all endpoints before going live

### 3. HTTPS Setup

#### Using Nginx Reverse Proxy

```nginx
server {
    listen 443 ssl;
    server_name your-domain.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

## Monitoring & Maintenance

### Health Checks

The application includes a health check endpoint:

```bash
curl http://your-domain/health
```

Response:
```json
{
  "status": "healthy"
}
```

### Logging

Logs are written to:
- **Console** (stdout) - For Docker/Kubernetes logging
- **File** (optional) - If `LOG_FILE_ENABLED=true`
- **Request logs** - All HTTP requests logged with timing

### Monitoring Recommendations

1. **Set up uptime monitoring**:
   - UptimeRobot (free)
   - Pingdom
   - StatusCake

2. **Error tracking**:
   - Sentry (https://sentry.io)
   - Rollbar
   - Bugsnag

3. **Performance monitoring**:
   - DataDog APM
   - New Relic
   - Prometheus + Grafana

4. **Log aggregation**:
   - Loggly
   - Papertrail
   - ELK Stack (Elasticsearch, Logstash, Kibana)

---

## Troubleshooting

### Issue: "OPENAI_API_KEY not set"

**Solution**:
1. Ensure `.env` file exists in `backend/` directory
2. Verify API key is set: `OPENAI_API_KEY=sk-...`
3. Restart the server

### Issue: Rate limiting too aggressive

**Solution**:
1. Edit `config.yaml` to increase limits
2. Or set environment variables:
   ```bash
   export RATE_LIMIT_PDD_GENERATION=20/minute
   export RATE_LIMIT_FILE_UPLOAD=10/minute
   ```
3. Restart server

### Issue: CORS errors in production

**Solution**:
1. Update `CORS_ORIGINS` environment variable:
   ```bash
   export CORS_ORIGINS=https://your-production-domain.com
   ```
2. Or edit `config.yaml`

### Issue: Docker build fails

**Solution**:
1. Ensure Docker daemon is running: `docker ps`
2. Clear Docker cache: `docker system prune -a`
3. Rebuild without cache: `docker-compose build --no-cache`

### Issue: High memory usage

**Solution**:
1. Reduce `SERVER_WORKERS` in environment
2. Implement request queuing
3. Add horizontal scaling (load balancer + multiple instances)

---

## Production Deployment Checklist

### Pre-Deployment

- [ ] All required environment variables set
- [ ] Configured for production (`APP_ENV=production`)
- [ ] Debug mode disabled (`APP_DEBUG=false`)
- [ ] HTTPS configured
- [ ] CORS set to production domain only
- [ ] Rate limiting enabled and tested
- [ ] Logging configured
- [ ] Health check endpoint accessible
- [ ] Database (if used) configured
- [ ] Backup strategy in place

### Post-Deployment

- [ ] Test all API endpoints
- [ ] Test file upload (PDF, DOCX, MP4)
- [ ] Test PDD generation
- [ ] Test export functionality
- [ ] Verify rate limiting works
- [ ] Check logs for errors
- [ ] Set up monitoring/alerting
- [ ] Document any custom configurations
- [ ] Create runbook for operations team

---

## Maintenance

### Updating the Application

#### Docker Deployment
```bash
docker-compose pull
docker-compose up -d --force-recreate
```

#### Traditional Deployment
```bash
git pull
pip install -r requirements.txt
# Restart server (systemd, supervisor, etc.)
```

### Scaling

#### Horizontal Scaling (Multiple Instances)

1. **Load Balancer Setup**:
   ```yaml
   # Example nginx upstream
   upstream backend {
       server backend1:8000;
       server backend2:8000;
       server backend3:8000;
   }
   ```

2. **Shared Session Storage** (future):
   - Redis for rate limiting
   - Database for persistence

#### Vertical Scaling (Single Instance)

1. **Increase workers**:
   ```bash
   export SERVER_WORKERS=8
   ```

2. **Add more resources**:
   - More CPU cores
   - More RAM
   - Faster disk I/O

---

## Support

For issues and questions:
- **Documentation**: See `TECHNICAL_DOCUMENTATION.md`
- **Issues**: Create a GitHub issue
- **Email**: [Your support email]

---

## Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [OpenAI API Documentation](https://platform.openai.com/docs/)

---

**Last Updated**: January 2026
**Version**: 1.0.0
