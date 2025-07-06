#!/usr/bin/env python3
"""
NXID Tokenomics - GUI EXE Builder
=================================
Auto-py-to-exe kullanarak GUI ile exe oluşturun
"""

import subprocess
import sys
import os

def install_auto_py_to_exe():
    """Auto-py-to-exe paketini yükle"""
    try:
        import auto_py_to_exe
        print("✅ auto-py-to-exe zaten yüklü")
        return True
    except ImportError:
        print("📦 auto-py-to-exe yükleniyor...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "auto-py-to-exe"])
            print("✅ auto-py-to-exe başarıyla yüklendi")
            return True
        except subprocess.CalledProcessError:
            print("❌ auto-py-to-exe yüklenemedi")
            return False

def create_config_json():
    """Auto-py-to-exe için config dosyası oluştur"""
    config = {
        "version": "auto-py-to-exe-configuration_v1",
        "pyinstallerOptions": [
            {
                "optionDest": "noconfirm",
                "value": True
            },
            {
                "optionDest": "filenames",
                "value": ["run.py"]
            },
            {
                "optionDest": "onefile", 
                "value": True
            },
            {
                "optionDest": "console",
                "value": True
            },
            {
                "optionDest": "icon_file",
                "value": "nxid-logo.ico" if os.path.exists("nxid-logo.ico") else ""
            },
            {
                "optionDest": "name",
                "value": "NXID_Tokenomics"
            },
            {
                "optionDest": "add_data",
                "value": [
                    "*.py;.",
                    "*.json;.",
                    "requirements.txt;."
                ]
            },
            {
                "optionDest": "hidden_import",
                "value": [
                    "streamlit",
                    "streamlit.web.cli", 
                    "pandas",
                    "numpy",
                    "plotly"
                ]
            }
        ]
    }
    
    import json
    with open('auto-py-to-exe-config.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    print("📄 Configuration dosyası oluşturuldu: auto-py-to-exe-config.json")

def launch_gui():
    """GUI'yi başlat"""
    print("🎨 GUI başlatılıyor...")
    print("💡 Tarayıcınızda auto-py-to-exe açılacak")
    print("📋 Önceden hazırlanan ayarları kullanabilirsiniz")
    
    try:
        subprocess.run([sys.executable, "-m", "auto_py_to_exe"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ GUI başlatılamadı: {e}")
        return False
    except KeyboardInterrupt:
        print("\n👋 GUI kapatıldı")
    
    return True

def main():
    """Ana fonksiyon"""
    print("🎯 NXID Enhanced Tokenomics - GUI EXE Builder")
    print("=" * 50)
    
    # Auto-py-to-exe yükle
    if not install_auto_py_to_exe():
        return False
    
    # Config oluştur
    create_config_json()
    
    # Kullanım talimatları
    print("\n📋 GUI Kullanım Talimatları:")
    print("1. Açılan tarayıcı penceresinde 'Configuration' sekmesine gidin")
    print("2. 'Load Configuration' butonuna tıklayın")
    print("3. 'auto-py-to-exe-config.json' dosyasını seçin")
    print("4. Ayarları kontrol edin:")
    print("   - Script Location: run.py")
    print("   - One File: ✅ (tek dosya)")
    print("   - Console Window: ✅ (debug için)")
    print("   - Icon: nxid-logo.ico (varsa)")
    print("5. 'CONVERT .PY TO .EXE' butonuna tıklayın")
    print("6. Build tamamlandıktan sonra 'output' klasöründe exe dosyanızı bulun")
    print("\n🚀 GUI başlatılıyor...")
    
    # GUI'yi başlat
    return launch_gui()

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)