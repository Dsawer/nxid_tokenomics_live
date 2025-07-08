#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NXID Tokenomics - Tkinter Desktop Wrapper (Unicode Fixed)
=========================================================
Kurulum gerektirmeyen desktop çözümü - Emoji hataları düzeltildi
"""

import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sys
import os
import threading
import time
import webbrowser
import requests
from urllib.parse import urljoin

# Unicode encoding için
import locale
import codecs

# Encoding düzelt
if sys.platform.startswith('win'):
    # Windows için UTF-8 encoding zorla
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.detach())

class NXIDDesktopApp:
    def __init__(self):
        self.root = tk.Tk()
        self.streamlit_process = None
        self.port = 8501
        self.url = f"http://localhost:{self.port}"
        
        self.setup_window()
        self.create_widgets()
        
    def setup_window(self):
        """Pencere ayarları"""
        self.root.title("NXID  Tokenomics Desktop")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 600)
        
        # Icon (eğer varsa)
        try:
            # Windows için
            self.root.iconbitmap("nxid-logo.ico")
        except:
            pass
        
        # Modern görünüm
        self.root.configure(bg="#0B1426")
        
        # Kapanış event'i
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def create_widgets(self):
        """Widget'ları oluştur"""
        # Ana frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Stil
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Title.TLabel', 
                       font=('Segoe UI', 16, 'bold'),
                       background='#0B1426',
                       foreground='#1B8EF2')
        
        # Başlık - Emoji kaldırıldı
        title_label = ttk.Label(main_frame, 
                               text="NXID  Tokenomics", 
                               style='Title.TLabel')
        title_label.pack(pady=(0, 20))
        
        # Status frame
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill='x', pady=(0, 10))
        
        self.status_label = ttk.Label(status_frame, text="Hazırlanıyor...")
        self.status_label.pack(side='left')
        
        # Progress bar
        self.progress = ttk.Progressbar(status_frame, mode='indeterminate')
        self.progress.pack(side='right', padx=(10, 0))
        
        # Butonlar frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill='x', pady=10)
        
        self.start_btn = ttk.Button(button_frame, 
                                   text=">> Uygulamayı Başlat", 
                                   command=self.start_application)
        self.start_btn.pack(side='left', padx=(0, 10))
        
        self.browser_btn = ttk.Button(button_frame, 
                                     text="Tarayıcıda Aç", 
                                     command=self.open_in_browser,
                                     state='disabled')
        self.browser_btn.pack(side='left', padx=(0, 10))
        
        self.stop_btn = ttk.Button(button_frame, 
                                  text="Durdur", 
                                  command=self.stop_application,
                                  state='disabled')
        self.stop_btn.pack(side='left')
        
        # Web frame - burada iframe benzeri bir şey olacak
        web_frame = ttk.LabelFrame(main_frame, text="NXID Tokenomics Uygulaması")
        web_frame.pack(fill='both', expand=True, pady=(10, 0))
        
        # Web content için text widget (iframe yerine)
        self.web_content = tk.Text(web_frame, 
                                  wrap='word',
                                  bg='#1e293b',
                                  fg='#e2e8f0',
                                  font=('Consolas', 10))
        self.web_content.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.web_content)
        scrollbar.pack(side='right', fill='y')
        self.web_content.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.web_content.yview)
        
        # İlk mesaj - Emoji kaldırıldı
        self.web_content.insert('1.0', '''
NXID  Tokenomics Desktop Uygulaması

Özellikler:
• Simple Interest Presale System
• Advanced Maturity Damping  
• Dynamic Staking with Price Velocity
• Real Circulating Supply Calculations
• 16-Quarter Scenario Analysis
•  Visualizations

Kullanım:
1. "Uygulamayı Başlat" butonuna tıklayın
2. Streamlit server başlatılacak
3. "Tarayıcıda Aç" ile uygulamayı görüntüleyin

Durum: Hazır - Başlatmak için butona tıklayın
''')
        self.web_content.config(state='disabled')
        
    def start_application(self):
        """Streamlit uygulamasını başlat"""
        self.update_status("Streamlit server başlatılıyor...")
        self.progress.start()
        self.start_btn.config(state='disabled')
        
        # Arka planda başlat
        thread = threading.Thread(target=self._start_streamlit_thread)
        thread.daemon = True
        thread.start()
        
    def _start_streamlit_thread(self):
        """Streamlit'i arka planda başlat"""
        try:
            # Ana uygulama dosyası kontrolü
            if not os.path.exists('main.py'):
                self.root.after(0, lambda: self.show_error("main.py dosyası bulunamadı!"))
                return
            
            # Streamlit komutunu oluştur
            cmd = [
                sys.executable, '-m', 'streamlit', 'run', 'main.py',
                '--server.headless=true',
                '--browser.gatherUsageStats=false',
                f'--server.port={self.port}',
                '--global.developmentMode=false',
                '--server.fileWatcherType=none'
            ]
            
            # Process başlat
            self.streamlit_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            )
            
            # Streamlit'in hazır olmasını bekle
            self.root.after(0, lambda: self.update_status("Streamlit hazırlanıyor..."))
            
            for i in range(30):  # 30 saniye bekle
                try:
                    response = requests.get(self.url, timeout=1)
                    if response.status_code == 200:
                        self.root.after(0, self._on_streamlit_ready)
                        return
                except:
                    pass
                time.sleep(1)
            
            # Timeout
            self.root.after(0, lambda: self.show_error("Streamlit başlatılamadı (timeout)"))
            
        except Exception as e:
            self.root.after(0, lambda: self.show_error(f"Başlatma hatası: {str(e)}"))
    
    def _on_streamlit_ready(self):
        """Streamlit hazır olduğunda"""
        self.progress.stop()
        self.update_status("SUCCESS: Streamlit başarıyla başlatıldı!")
        
        self.browser_btn.config(state='normal')
        self.stop_btn.config(state='normal')
        
        # Otomatik tarayıcıda aç
        self.open_in_browser()
        
        # İçerik güncelle - Emoji kaldırıldı
        self.web_content.config(state='normal')
        self.web_content.delete('1.0', 'end')
        self.web_content.insert('1.0', f'''
SUCCESS: NXID  Tokenomics Başarıyla Başlatıldı!

URL: {self.url}
Durum: Aktif ve çalışıyor
Tarayıcınızda otomatik açıldı

İpuçları:
• Tarayıcı sekmesini kapatırsanız "Tarayıcıda Aç" butonuyla tekrar açabilirsiniz
• Uygulamayı tamamen kapatmak için "Durdur" butonunu kullanın
• Bu pencereyi küçültebilir, arka planda çalıştırabilirsiniz

NXID Tokenomics şu anda çalışıyor ve kullanıma hazır!

Tarayıcınızdaki sekmede:
• Sol panelden parametreleri ayarlayın
• Scenario seçin (Bear/Base/Bull)
• " NXID Tokenomics Launch" butonuna tıklayın
• Sonuçları analiz edin
''')
        self.web_content.config(state='disabled')
    
    def open_in_browser(self):
        """Tarayıcıda aç"""
        try:
            webbrowser.open(self.url)
            self.update_status("Tarayıcıda açıldı: " + self.url)
        except Exception as e:
            self.show_error(f"Tarayıcı açma hatası: {str(e)}")
    
    def stop_application(self):
        """Uygulamayı durdur"""
        if self.streamlit_process:
            self.streamlit_process.terminate()
            self.streamlit_process = None
        
        self.update_status("Streamlit durduruldu")
        self.start_btn.config(state='normal')
        self.browser_btn.config(state='disabled')
        self.stop_btn.config(state='disabled')
        self.progress.stop()
        
        # İçerik güncelle - Emoji kaldırıldı
        self.web_content.config(state='normal')
        self.web_content.delete('1.0', 'end')
        self.web_content.insert('1.0', '''
NXID Tokenomics Durduruldu

Uygulama başarıyla durduruldu. Tekrar başlatmak için "Uygulamayı Başlat" butonuna tıklayın.

Durum: Durduruldu
Tekrar başlatmaya hazır
''')
        self.web_content.config(state='disabled')
    
    def update_status(self, message):
        """Status güncelle"""
        self.status_label.config(text=message)
        
    def show_error(self, message):
        """Hata göster"""
        self.progress.stop()
        self.start_btn.config(state='normal')
        self.update_status("ERROR: " + message)
        messagebox.showerror("Hata", message)
    
    def on_closing(self):
        """Kapanış işlemi"""
        if self.streamlit_process:
            self.streamlit_process.terminate()
        self.root.destroy()
    
    def run(self):
        """Uygulamayı çalıştır"""
        self.root.mainloop()

def main():
    """Ana fonksiyon"""
    print("NXID  Tokenomics Desktop (Tkinter)")
    print("===========================================")
    
    try:
        app = NXIDDesktopApp()
        app.run()
    except Exception as e:
        print(f"Desktop uygulama hatası: {str(e)}")
        input("Çıkmak için Enter'a basın...")

if __name__ == "__main__":
    main()