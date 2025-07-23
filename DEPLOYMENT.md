# Deployment Guide

This guide covers various deployment options for the MCP Web Search Answer application.

## 🚀 Quick Deployment Options

### 1. Local Development

```bash
# Clone the repository
git clone https://github.com/yourusername/mcp_web_search_answer.git
cd mcp_web_search_answer

# Set up environment
cp .env.example .env
# Edit .env with your API keys

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

### 2. Docker Deployment

#### Single Container
```bash
# Build the image
docker build -t mcp-web-search-answer .

# Run the container
docker run -d \
  --name mcp-web-search \
  -p 8000:8000 \
  -e GEMINI_API_KEY=your_key \
  -e SERPAPI_KEY=your_key \
  mcp-web-search-answer
```

#### Docker Compose
```bash
# Copy environment file
cp .env.example .env
# Edit .env with your API keys

# Start all services
docker-compose up -d

# With caching (Redis)
docker-compose --profile with-cache up -d

# With monitoring
docker-compose --profile monitoring up -d
```

### 3. Cloud Deployment

#### AWS ECS
```bash
# Build and push to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 123456789012.dkr.ecr.us-east-1.amazonaws.com
docker build -t mcp-web-search-answer .
docker tag mcp-web-search-answer:latest 123456789012.dkr.ecr.us-east-1.amazonaws.com/mcp-web-search-answer:latest
docker push 123456789012.dkr.ecr.us-east-1.amazonaws.com/mcp-web-search-answer:latest

# Deploy using ECS task definition
aws ecs update-service --cluster your-cluster --service mcp-web-search --force-new-deployment
```

#### Google Cloud Run
```bash
# Build and deploy
gcloud builds submit --tag gcr.io/your-project/mcp-web-search-answer
gcloud run deploy mcp-web-search \
  --image gcr.io/your-project/mcp-web-search-answer \
  --platform managed \
  --region us-central1 \
  --set-env-vars GEMINI_API_KEY=your_key,SERPAPI_KEY=your_key
```

#### Azure Container Instances
```bash
# Create resource group
az group create --name mcp-rg --location eastus

# Deploy container
az container create \
  --resource-group mcp-rg \
  --name mcp-web-search \
  --image your-registry/mcp-web-search-answer:latest \
  --dns-name-label mcp-web-search \
  --ports 8000 \
  --environment-variables GEMINI_API_KEY=your_key SERPAPI_KEY=your_key
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `GEMINI_API_KEY` | Google Gemini API key | Yes | - |
| `SERPAPI_KEY` | SerpAPI key for web search | Yes | - |
| `LOG_LEVEL` | Logging level | No | `INFO` |
| `MAX_RETRIES` | Max API retry attempts | No | `3` |
| `TIMEOUT` | Request timeout in seconds | No | `30` |

### Production Settings

Create a `.env.production` file:
```bash
GEMINI_API_KEY=your_production_key
SERPAPI_KEY=your_production_key
LOG_LEVEL=WARNING
MAX_RETRIES=5
TIMEOUT=60
```

## 🔒 Security Considerations

### API Key Management

1. **Never commit API keys to version control**
2. **Use environment variables or secret management services**
3. **Rotate keys regularly**
4. **Use different keys for different environments**

### Network Security

```bash
# Use HTTPS in production
# Configure firewall rules
# Implement rate limiting
# Use VPC/private networks when possible
```

### Container Security

```dockerfile
# Use non-root user
USER appuser

# Scan for vulnerabilities
docker scan mcp-web-search-answer

# Use minimal base images
FROM python:3.11-slim
```

## 📊 Monitoring and Logging

### Health Checks

The application includes health check endpoints:

```bash
# Docker health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')" || exit 1

# Kubernetes liveness probe
livenessProbe:
  httpGet:
    path: /health
    port: 8000
  initialDelaySeconds: 30
  periodSeconds: 10
```

### Logging

Configure structured logging:

```python
import logging
import structlog

# Configure logging
logging.basicConfig(
    format="%(message)s",
    stream=sys.stdout,
    level=logging.INFO,
)

structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)
```

### Metrics

Enable Prometheus metrics:

```python
from prometheus_client import Counter, Histogram, generate_latest

# Metrics
REQUEST_COUNT = Counter('requests_total', 'Total requests', ['method', 'endpoint'])
REQUEST_DURATION = Histogram('request_duration_seconds', 'Request duration')

# Expose metrics endpoint
@app.route('/metrics')
def metrics():
    return generate_latest()
```

## 🚀 CI/CD Pipeline

The project includes GitHub Actions workflows:

### Continuous Integration
- **Code quality checks** (flake8, black, isort)
- **Security scanning** (bandit, safety)
- **Multi-version testing** (Python 3.8-3.12)
- **Documentation validation**

### Continuous Deployment
- **Automated Docker builds**
- **Multi-environment deployment**
- **Release automation**
- **Rollback capabilities**

### Manual Deployment

```bash
# Trigger manual deployment
gh workflow run deploy.yml -f environment=staging

# Check deployment status
gh run list --workflow=deploy.yml
```

## 🔄 Scaling

### Horizontal Scaling

```yaml
# Kubernetes deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mcp-web-search
spec:
  replicas: 3
  selector:
    matchLabels:
      app: mcp-web-search
  template:
    metadata:
      labels:
        app: mcp-web-search
    spec:
      containers:
      - name: mcp-web-search
        image: mcp-web-search-answer:latest
        ports:
        - containerPort: 8000
        env:
        - name: GEMINI_API_KEY
          valueFrom:
            secretKeyRef:
              name: api-keys
              key: gemini-key
```

### Load Balancing

```nginx
# Nginx configuration
upstream mcp_backend {
    server mcp-web-search-1:8000;
    server mcp-web-search-2:8000;
    server mcp-web-search-3:8000;
}

server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://mcp_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 🛠️ Troubleshooting

### Common Issues

1. **API Key Errors**
   ```bash
   # Check environment variables
   echo $GEMINI_API_KEY
   echo $SERPAPI_KEY
   
   # Validate keys
   curl -H "Authorization: Bearer $GEMINI_API_KEY" https://generativelanguage.googleapis.com/v1/models
   ```

2. **Network Issues**
   ```bash
   # Check connectivity
   curl -I https://serpapi.com
   curl -I https://generativelanguage.googleapis.com
   
   # Check DNS resolution
   nslookup serpapi.com
   ```

3. **Container Issues**
   ```bash
   # Check container logs
   docker logs mcp-web-search
   
   # Debug container
   docker exec -it mcp-web-search /bin/bash
   
   # Check resource usage
   docker stats mcp-web-search
   ```

### Performance Tuning

1. **Optimize API calls**
   - Implement caching
   - Use connection pooling
   - Set appropriate timeouts

2. **Resource allocation**
   ```yaml
   resources:
     requests:
       memory: "256Mi"
       cpu: "250m"
     limits:
       memory: "512Mi"
       cpu: "500m"
   ```

3. **Database optimization** (if using caching)
   ```bash
   # Redis optimization
   redis-cli CONFIG SET maxmemory 256mb
   redis-cli CONFIG SET maxmemory-policy allkeys-lru
   ```

## 📞 Support

For deployment issues:

1. Check the [troubleshooting section](#troubleshooting)
2. Review [GitHub Issues](https://github.com/yourusername/mcp_web_search_answer/issues)
3. Create a new issue with deployment details
4. Join our community discussions

## 🔄 Updates and Maintenance

### Regular Maintenance

```bash
# Update dependencies
pip install --upgrade -r requirements.txt

# Security updates
docker pull python:3.11-slim
docker build -t mcp-web-search-answer:latest .

# Database maintenance (if using caching)
redis-cli FLUSHDB
```

### Backup and Recovery

```bash
# Backup configuration
tar -czf backup-$(date +%Y%m%d).tar.gz .env participants.yaml

# Backup logs
tar -czf logs-backup-$(date +%Y%m%d).tar.gz logs/

# Recovery
tar -xzf backup-20241219.tar.gz
```