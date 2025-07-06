#NXID_tokenomics.py
"""
NXID Advanced Tokenomics v3.1 - Quick Run Script
===============================================
Hızlı başlatma script'i - projeyi kolayca çalıştırın
"""

import subprocess
import sys
import os

def check_requirements():
    """Gerekli paketlerin yüklü olup olmadığını kontrol et"""
    required_packages = [
        'streamlit',
        'pandas', 
        'numpy',
        'plotly'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    return missing_packages

def install_requirements():
    """Gerekli paketleri yükle"""
    print("📦 Gerekli paketler yükleniyor...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Tüm paketler başarıyla yüklendi!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Paket yükleme hatası!")
        return False

def check_files():
    """Gerekli dosyaların varlığını kontrol et"""
    required_files = [
        'main.py',
        'config.py',
        'models.py',
        'visualizations.py',
        'sidebar.py',
        'analytics.py',
        'utils.py',
        'requirements.txt'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    return missing_files

def run_app():
    """Streamlit uygulamasını çalıştır"""
    print(" NXID Advanced Tokenomics v3.1 başlatılıyor...")
    print("📊 Uygulama tarayıcınızda açılacak...")
    print("🔗 URL: http://localhost:8501")
    print("⏹️  Durdurmak için Ctrl+C basın")
    print("-" * 50)
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "main.py",
            "--server.headless", "true",
            "--browser.gatherUsageStats", "false"
        ])
    except KeyboardInterrupt:
        print("\n🛑 Uygulama durduruldu.")
    except Exception as e:
        print(f"❌ Hata: {e}")

def main():
    """Ana fonksiyon"""
    print("=" * 60)
    print(" NXID ADVANCED TOKENOMICS v3.1")
    print("   Enhanced Professional Analysis Platform")
    print("=" * 60)
    
    # Dosya kontrolü
    print("📁 Dosyalar kontrol ediliyor...")
    missing_files = check_files()
    if missing_files:
        print(f"❌ Eksik dosyalar: {', '.join(missing_files)}")
        print("💡 Tüm dosyaların aynı klasörde olduğundan emin olun.")
        return
    
    print("✅ Tüm dosyalar mevcut!")
    
    # Paket kontrolü
    print("📦 Paketler kontrol ediliyor...")
    missing_packages = check_requirements()
    
    if missing_packages:
        print(f"⚠️  Eksik paketler: {', '.join(missing_packages)}")
        print("🔧 Paketler otomatik yüklenecek...")
        
        if not install_requirements():
            print("❌ Paket yükleme başarısız. Manuel yükleme:")
            print("   pip install -r requirements.txt")
            return
    else:
        print("✅ Tüm paketler yüklü!")
    
    # Uygulama başlat
    print("\n Hazırlanıyor...")
    run_app()

if __name__ == "__main__":
    main()