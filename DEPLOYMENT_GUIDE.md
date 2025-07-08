# NXID  Tokenomics - Web Deployment Guide

## Deployment Options

### Option 1: Streamlit Cloud (Recommended - FREE!)

1. **GitHub'a push et:**
   ```bash
   git add .
   git commit -m "NXID  Tokenomics"
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
