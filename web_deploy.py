#!/usr/bin/env python3
"""
NXID Enhanced Tokenomics - Web Deployment Helper (FIXED)
=======================================================
Python olmayan bilgisayarlar için web deployment - Unicode hatası düzeltildi
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

class WebDeploymentHelper:
    """Web deployment yardımcı sınıfı"""
    
    def __init__(self):
        self.root_dir = Path(__file__).parent
        
    def prepare_for_streamlit_cloud(self):
        """Streamlit Cloud için hazırla"""
        print("☁️ Preparing for Streamlit Cloud...")
        
        # .streamlit klasörü oluştur
        streamlit_dir = self.root_dir / ".streamlit"
        streamlit_dir.mkdir(exist_ok=True)
        
        # config.toml oluştur
        config_content = """[theme]
primaryColor = "#1B8EF2"
backgroundColor = "#0B1426"  
secondaryBackgroundColor = "#1e293b"
textColor = "#FFFFFF"

[server]
headless = true
port = 8501
enableCORS = false
enableXsrfProtection = false

[browser]
gatherUsageStats = false
"""
        
        with open(streamlit_dir / "config.toml", "w", encoding="utf-8") as f:
            f.write(config_content)
        
        # secrets.toml örneği
        secrets_example = """# Streamlit Cloud Secrets Example
# Add your secrets here if needed

[database]
# host = "your-db-host"
# username = "your-username"  
# password = "your-password"

[api]
# api_key = "your-api-key"
"""
        
        with open(streamlit_dir / "secrets.toml.example", "w", encoding="utf-8") as f:
            f.write(secrets_example)
        
        print("✅ Streamlit Cloud config created!")
        return True
    
    def create_requirements_txt(self):
        """Web deployment için requirements.txt"""
        print("📦 Creating web requirements.txt...")
        
        web_requirements = """# NXID Enhanced Tokenomics - Web Deployment Requirements
streamlit>=1.33,<1.36
pandas>=2.2,<2.3
numpy>=2.0,<2.2
plotly>=5.19,<6.0

# Optional performance boosters for cloud
streamlit-option-menu>=0.3.0
streamlit-aggrid>=0.3.0
"""
        
        with open(self.root_dir / "requirements.txt", "w", encoding="utf-8") as f:
            f.write(web_requirements)
        
        print("✅ Web requirements.txt created!")
        return True
    
    def create_dockerfile(self):
        """Docker deployment için Dockerfile"""
        print("🐳 Creating Dockerfile...")
        
        dockerfile_content = """# NXID Enhanced Tokenomics - Docker Image
FROM python:3.11-slim

# Working directory
WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y \\
    build-essential \\
    curl \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run command
ENTRYPOINT ["streamlit", "run", "NXID_tokenomics.py", "--server.port=8501", "--server.address=0.0.0.0"]
"""
        
        with open(self.root_dir / "Dockerfile", "w", encoding="utf-8") as f:
            f.write(dockerfile_content)
        
        # .dockerignore
        dockerignore_content = """__pycache__
*.pyc
*.pyo
*.pyd
.Python
env
pip-log.txt
pip-delete-this-directory.txt
.tox
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.log
.git
.mypy_cache
.pytest_cache
.hypothesis

.DS_Store
.vscode
*.egg-info

# Local config files
*.json
logs/
dist/
build/
"""
        
        with open(self.root_dir / ".dockerignore", "w", encoding="utf-8") as f:
            f.write(dockerignore_content)
        
        print("✅ Dockerfile created!")
        return True
    
    def create_docker_compose(self):
        """Docker Compose file oluştur"""
        print("🐳 Creating docker-compose.yml...")
        
        compose_content = """version: '3.8'

services:
  nxid-tokenomics:
    build: .
    container_name: nxid-enhanced-tokenomics
    ports:
      - "8501:8501"
    environment:
      - STREAMLIT_SERVER_HEADLESS=true
      - STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
    volumes:
      - ./data:/app/data  # Config persistence
      - ./logs:/app/logs  # Log persistence
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8501/_stcore/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  # Optional: Add reverse proxy
  nginx:
    image: nginx:alpine
    container_name: nxid-nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - nxid-tokenomics
    restart: unless-stopped
"""
        
        with open(self.root_dir / "docker-compose.yml", "w", encoding="utf-8") as f:
            f.write(compose_content)
        
        print("✅ Docker Compose created!")
        return True
    
    def create_heroku_files(self):
        """Heroku deployment dosyaları"""
        print("🚀 Creating Heroku files...")
        
        # Procfile
        with open(self.root_dir / "Procfile", "w", encoding="utf-8") as f:
            f.write("web: streamlit run NXID_tokenomics.py --server.port=$PORT --server.address=0.0.0.0\n")
        
        # runtime.txt
        with open(self.root_dir / "runtime.txt", "w", encoding="utf-8") as f:
            f.write("python-3.11.6\n")
        
        # app.json
        app_json = """{
  "name": "NXID Enhanced Tokenomics",
  "description": "Professional cryptocurrency tokenomics analysis platform",
  "image": "heroku/python",
  "repository": "https://github.com/your-username/nxid-enhanced-tokenomics",
  "keywords": ["streamlit", "cryptocurrency", "tokenomics", "analysis"],
  "env": {
    "STREAMLIT_SERVER_HEADLESS": {
      "description": "Run Streamlit in headless mode",
      "value": "true"
    },
    "STREAMLIT_BROWSER_GATHER_USAGE_STATS": {
      "description": "Disable usage stats",
      "value": "false"
    }
  },
  "buildpacks": [
    {
      "url": "heroku/python"
    }
  ],
  "stack": "heroku-22"
}"""
        
        with open(self.root_dir / "app.json", "w", encoding="utf-8") as f:
            f.write(app_json)
        
        print("✅ Heroku files created!")
        return True
    
    def create_railway_config(self):
        """Railway deployment config"""
        print("🚂 Creating Railway config...")
        
        # railway.json
        railway_config = """{
  "deploy": {
    "startCommand": "streamlit run NXID_tokenomics.py --server.port=$PORT --server.address=0.0.0.0",
    "healthcheckPath": "/_stcore/health",
    "healthcheckTimeout": 100
  }
}"""
        
        with open(self.root_dir / "railway.json", "w", encoding="utf-8") as f:
            f.write(railway_config)
        
        print("✅ Railway config created!")
        return True
    
    def create_deployment_guide(self):
        """Deployment guide oluştur - ASCII karakterler ile"""
        print("📖 Creating deployment guide...")
        
        guide_content = """# NXID Enhanced Tokenomics - Web Deployment Guide

## Deployment Options

### Option 1: Streamlit Cloud (Recommended - FREE!)

1. **GitHub'a push et:**
   ```bash
   git add .
   git commit -m "NXID Enhanced Tokenomics"
   git push origin main
   ```

2. **Streamlit Cloud'da deploy et:**
   - https://share.streamlit.io adresine git
   - GitHub repo'nu connect et
   - `NXID_tokenomics.py` dosyasini sec
   - Deploy butonuna bas

3. **Hazir!** Link'i herkesle paylas

### Option 2: Heroku (FREE tier kaldirildi)

```bash
# Heroku CLI install et
# heroku create nxid-tokenomics
# git push heroku main
```

### Option 3: Railway (FREE + Kolay)

1. **Railway.app'e git**
2. **GitHub connect et**
3. **Deploy from GitHub**
4. **Otomatik deploy olur**

### Option 4: Render (FREE)

1. **render.com'a git**
2. **New Web Service**
3. **GitHub repo connect et**
4. **Build & Start Command:**
   ```
   pip install -r requirements.txt
   streamlit run NXID_tokenomics.py --server.port=$PORT --server.address=0.0.0.0
   ```

### Option 5: Docker (Her yerde calisir)

```bash
# Build
docker build -t nxid-tokenomics .

# Run
docker run -p 8501:8501 nxid-tokenomics

# Docker Compose ile
docker-compose up
```

### Option 6: Replit (Cok Kolay)

1. **replit.com'a git**
2. **Import from GitHub**
3. **Run butonuna bas**
4. **Otomatik calisir**

## Deployment Links

| Platform | Maliyet | Kolay | Recommended |
|----------|---------|--------|-------------|
| **Streamlit Cloud** | FREE | 5/5 | YES |
| **Railway** | $5/mo | 4/5 | YES |
| **Render** | FREE | 4/5 | YES |
| **Replit** | FREE | 5/5 | YES |
| **Heroku** | $7/mo | 3/5 | Expensive |

## En Hizli Deploy

### 1. Streamlit Cloud (3 dakika)
```bash
git add . && git commit -m "deploy" && git push
# share.streamlit.io'da deploy et
```

### 2. Replit (1 dakika)
- Repo'yu import et
- Run butonuna bas
- Hazir!

## Environment Variables

Gerekirse sunlari ekle:

```env
STREAMLIT_SERVER_HEADLESS=true
STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
STREAMLIT_THEME_PRIMARY_COLOR=#1B8EF2
```

## Custom Domain

Deploy ettikten sonra custom domain baglayabilirsin:
- **nxid-tokenomics.yourdomain.com**
- DNS CNAME record ekle
- Platform'da domain verify et

## Mobile Support

Streamlit otomatik responsive. Mobile'da da mukemmel calisir!

## Sonuc

En kolayi: **Streamlit Cloud** veya **Replit**
- Bedava
- 5 dakikada hazir  
- Otomatik SSL
- Guvenilir uptime
- Kolay paylasim

Deploy ettikten sonra link'i herkesle paylas!
"""
        
        with open(self.root_dir / "DEPLOYMENT_GUIDE.md", "w", encoding="utf-8") as f:
            f.write(guide_content)
        
        print("✅ Deployment guide created!")
        return True
    
    def prepare_all_deployments(self):
        """Tüm deployment seçeneklerini hazırla"""
        print("🌐 Preparing all deployment options...")
        
        steps = [
            ("Streamlit Cloud config", self.prepare_for_streamlit_cloud),
            ("Web requirements.txt", self.create_requirements_txt),
            ("Docker files", self.create_dockerfile),
            ("Docker Compose", self.create_docker_compose),
            ("Heroku files", self.create_heroku_files),
            ("Railway config", self.create_railway_config),
            ("Deployment guide", self.create_deployment_guide)
        ]
        
        for step_name, step_func in steps:
            print(f"\n🔄 {step_name}...")
            if not step_func():
                print(f"❌ {step_name} failed!")
                return False
        
        print("\n✅ All deployment options prepared!")
        print("\n🎯 Quick deployment commands:")
        print("📋 Streamlit Cloud: push to GitHub then deploy at share.streamlit.io")
        print("🐳 Docker: docker build -t nxid . && docker run -p 8501:8501 nxid")
        print("🚂 Railway: git push origin main (auto-deploys)")
        print("🎭 Replit: Import GitHub repo and click Run")
        
        return True

def main():
    """Ana fonksiyon"""
    print("🌐 NXID Enhanced Tokenomics - Web Deployment Helper")
    print("=" * 52)
    
    deployer = WebDeploymentHelper()
    
    if deployer.prepare_all_deployments():
        print("\n🎉 SUCCESS! Ready for web deployment!")
        print("\nRecommended: Streamlit Cloud (free + easy)")
    else:
        print("\n❌ Deployment preparation failed!")

if __name__ == "__main__":
    main()